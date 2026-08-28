# -*- coding: utf-8 -*-
"""
AI 宠物顾问的 LangGraph 编排。

图很简单，只有两个节点：

    agent ──(需要调用工具)──> tools ──> agent
      │
      └──(直接作答)──> END

工具调用轮数设了上限。没有上限时，模型可能反复调同一个工具形成死循环，
每一轮都是真金白银的上游调用。
"""

from __future__ import annotations

import logging
import os

from langchain_core.messages import (
	AIMessage,
	AIMessageChunk,
	HumanMessage,
	SystemMessage,
	ToolMessage,
)
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from typing_extensions import Annotated, TypedDict

from .tools import get_tools

logger = logging.getLogger(__name__)

LONGCAT_API_URL = 'https://api.longcat.chat/openai/v1'
DEFAULT_MODEL = 'LongCat-Flash-Chat'
MAX_TOOL_ROUNDS = 3
MAX_TOKENS = 1200
TEMPERATURE = 0.7

SYSTEM_PROMPT = """你是吉祥宠物商城的 AI 宠物顾问。

关于本店（重要）：
- 本店只售宠物用品：主粮、零食、玩具、清洁、保健、护理、牵引、洗澡、服饰。
- 本店不售活体宠物。若用户想买猫狗本体，直接说明本店不售活体，可以帮他准备用品。

工作方式：
- 涉及用量、周期、操作步骤（如换粮过渡、驱虫间隔、洗护频率）时，先用
  search_knowledge_base 查店内资料，依据资料回答，不要凭记忆编造数字。
- 用户问「有没有卖」「推荐几款」「预算多少以内」时，用 search_products
  查真实在售商品，只推荐查到的商品，不要虚构商品名或价格。
- 知识库和商品库都没有结果时，如实说明，并给出通用建议，不要假装店里有。

边界：
- 只回答宠物相关问题。用户问编程、政治、金融、人类医疗等，礼貌地引导回宠物话题。
- 出现呕吐不止、抽搐、呼吸困难、误食异物等急症迹象时，第一句就建议立即就医，
  不要先讲护理建议。
- 你不能下单、不能修改订单、不能查看用户账户信息。用户要求这些时，引导他到
  对应页面自行操作。

回答风格：
- 专业、简洁、有条理，用 markdown。
- 不要使用 emoji。
- 涉及剂量和周期时明确说明依据来自店内资料，并提示以产品说明书为准。"""


class AgentState(TypedDict):
	"""图的状态。messages 累积整轮对话，包括工具调用记录。"""

	messages: Annotated[list, lambda existing, new: existing + new]
	tool_rounds: int


def _get_api_key() -> str:
	key = os.environ.get('LONGCAT_API_KEY', '').strip()
	if not key:
		raise RuntimeError('未配置 LONGCAT_API_KEY。')
	return key


def _build_llm():
	"""
	LongCat 兼容 OpenAI 的 chat completions 格式，所以直接用 ChatOpenAI
	指向它的 base_url，不需要自己实现 ChatModel。

	streaming 恒为 True：stream_mode='messages' 依赖底层模型产出增量，
	关掉的话流式接口只会在最后收到一整块内容。非流式调用走 invoke()，
	不受影响。
	"""
	from langchain_openai import ChatOpenAI

	return ChatOpenAI(
		model=os.environ.get('LONGCAT_MODEL') or DEFAULT_MODEL,
		api_key=_get_api_key(),
		base_url=os.environ.get('LONGCAT_BASE_URL') or LONGCAT_API_URL,
		max_tokens=MAX_TOKENS,
		temperature=TEMPERATURE,
		streaming=True,
		timeout=60,
		max_retries=1,
	)


def _agent_node(state: AgentState) -> dict:
	llm = _build_llm().bind_tools(get_tools())
	response = llm.invoke(state['messages'])
	return {'messages': [response], 'tool_rounds': state.get('tool_rounds', 0)}


def _should_continue(state: AgentState) -> str:
	"""决定是继续调工具还是收尾。"""
	last = state['messages'][-1]
	calls = getattr(last, 'tool_calls', None)
	if not calls:
		return END
	# 到达轮数上限就强制作答，避免无限调用消耗上游额度
	if state.get('tool_rounds', 0) >= MAX_TOOL_ROUNDS:
		logger.warning('工具调用达到上限 %s，强制结束。', MAX_TOOL_ROUNDS)
		return END
	return 'tools'


def _tools_node_wrapper(state: AgentState) -> dict:
	node = ToolNode(get_tools())
	result = node.invoke(state)
	messages = result['messages'] if isinstance(result, dict) else result
	return {'messages': messages, 'tool_rounds': state.get('tool_rounds', 0) + 1}


_compiled_graph = None


def get_graph():
	"""编译后的图缓存起来复用：每次请求重新编译是白费开销。"""
	global _compiled_graph
	if _compiled_graph is not None:
		return _compiled_graph

	builder = StateGraph(AgentState)
	builder.add_node('agent', _agent_node)
	builder.add_node('tools', _tools_node_wrapper)
	builder.add_edge(START, 'agent')
	builder.add_conditional_edges('agent', _should_continue, {'tools': 'tools', END: END})
	builder.add_edge('tools', 'agent')

	_compiled_graph = builder.compile()
	return _compiled_graph


def build_messages(history: list[dict], question: str) -> list:
	"""
	把会话历史转成 LangChain 消息。

	只接受 user / assistant 两种角色 —— system 由服务端固定注入，
	不允许调用方通过历史塞入自己的系统指令来改写行为。
	"""
	messages = [SystemMessage(content=SYSTEM_PROMPT)]
	for item in history:
		role = item.get('role')
		content = (item.get('content') or '').strip()
		if not content:
			continue
		if role == 'assistant':
			messages.append(AIMessage(content=content))
		elif role == 'user':
			messages.append(HumanMessage(content=content))
	if question:
		messages.append(HumanMessage(content=question))
	return messages


def run_agent(history: list[dict], question: str) -> dict:
	"""
	同步跑完一轮，返回最终回答、用过的工具和引用到的知识库分片。

	引用 id 不从 ToolMessage 的文本里解析 —— 那样既脆弱又要求工具把 id
	混进给模型看的正文。改由 tools.py 在检索时记录到 recorder，这里直接取。
	"""
	from .tools import citation_recorder

	graph = get_graph()
	state = {'messages': build_messages(history, question), 'tool_rounds': 0}

	with citation_recorder() as cited:
		result = graph.invoke(state)

	messages = result['messages']
	answer = ''
	tools_used = []
	for message in messages:
		if isinstance(message, ToolMessage):
			tools_used.append(message.name)
		elif isinstance(message, AIMessage) and message.content:
			answer = message.content

	return {
		'answer': (answer or '').strip() or '抱歉，我暂时无法回答这个问题。',
		'tools_used': tools_used,
		'tool_rounds': result.get('tool_rounds', 0),
		'cited_chunk_ids': list(cited),
	}


def stream_agent(history: list[dict], question: str):
	"""
	逐 token 流式跑一轮。产出 (事件类型, 数据) 元组：

	    ('tool_start', 工具名)   开始调用某个工具
	    ('token', 文本片段)      正文增量
	    ('final', 汇总 dict)     结束，带完整答案/引用/工具列表

	为什么要区分事件：模型在决定调用工具时也会产生 token（工具参数的
	JSON），那些不是给用户看的内容。只有工具调用结束后、模型基于结果
	组织的那段输出才是正文。这里靠 tool_calls 是否存在来判断。
	"""
	from .tools import citation_recorder

	graph = get_graph()
	state = {'messages': build_messages(history, question), 'tool_rounds': 0}

	answer_parts: list[str] = []
	tools_used: list[str] = []

	with citation_recorder() as cited:
		for chunk, meta in graph.stream(state, stream_mode='messages'):
			node = (meta or {}).get('langgraph_node')

			if isinstance(chunk, ToolMessage):
				if chunk.name and chunk.name not in tools_used:
					tools_used.append(chunk.name)
				continue

			if not isinstance(chunk, (AIMessage, AIMessageChunk)):
				continue

			# 模型正在拼工具调用参数，这一段不是正文
			if getattr(chunk, 'tool_calls', None) or getattr(chunk, 'tool_call_chunks', None):
				for call in getattr(chunk, 'tool_calls', None) or []:
					name = call.get('name') if isinstance(call, dict) else None
					if name:
						yield ('tool_start', name)
				continue

			content = chunk.content
			# 部分模型会把 content 拆成结构化块，取其中的文本
			if isinstance(content, list):
				content = ''.join(
					part.get('text', '') for part in content if isinstance(part, dict)
				)
			if content and node == 'agent':
				answer_parts.append(content)
				yield ('token', content)

		answer = ''.join(answer_parts).strip()
		yield ('final', {
			'answer': answer or '抱歉，我暂时无法回答这个问题。',
			'tools_used': tools_used,
			'cited_chunk_ids': list(cited),
		})

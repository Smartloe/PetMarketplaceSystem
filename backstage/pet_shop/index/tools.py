# -*- coding: utf-8 -*-
"""
Agent 可调用的工具。

两条硬规则：

1. 全部只读。工具不写库、不下单、不改用户数据 —— 模型的输出不可预测，
   不能让它触发有副作用的操作。
2. 不暴露内部字段。商品只返回展示所需的字段，不返回 cost_price（进价）
   这类商业敏感数据 —— 模型会把拿到的东西原样说给用户。
"""

from __future__ import annotations

import contextlib
import logging
import threading

from langchain_core.tools import tool

from commodity.models import CommodityInfos

from . import rag

logger = logging.getLogger(__name__)

# 记录本轮检索命中的分片 id，供 views 层展示引用来源。
# 用 threading.local 而不是模块级 list：Django 并发处理请求时，多个线程
# 共享模块状态会让 A 用户的引用混进 B 用户的回答里。
_local = threading.local()


@contextlib.contextmanager
def citation_recorder():
	"""在 with 块内收集知识库检索命中的分片 id。"""
	previous = getattr(_local, 'cited', None)
	_local.cited = []
	try:
		yield _local.cited
	finally:
		# 恢复外层状态，支持嵌套调用
		_local.cited = previous


def _record_citations(chunk_ids: list[int]) -> None:
	cited = getattr(_local, 'cited', None)
	if cited is None:
		return
	for chunk_id in chunk_ids:
		if chunk_id not in cited:
			cited.append(chunk_id)

# 单次搜索返回的商品数上限，避免把整个目录塞进 prompt
MAX_PRODUCTS = 5
MAX_KNOWLEDGE_CHUNKS = 4


@tool
def search_products(keyword: str, max_price: float | None = None) -> str:
	"""
	搜索商城在售的宠物用品。

	用于回答"有没有卖 X""推荐几款 Y""预算 200 以内有什么"这类问题。
	本商城只售宠物用品（主粮、零食、玩具、清洁、保健、护理、牵引、洗澡、
	服饰等），不售活体宠物。

	Args:
		keyword: 商品关键词，例如「幼犬主粮」「驱虫」「猫砂」。
		max_price: 可选的价格上限（元）。
	"""
	keyword = (keyword or '').strip()
	if not keyword:
		return '需要提供搜索关键词。'

	queryset = CommodityInfos.objects.filter(
		sku_title__icontains=keyword,
	).select_related('types')

	if max_price is not None:
		try:
			queryset = queryset.filter(price__lte=float(max_price))
		except (TypeError, ValueError):
			pass

	# 有货的排前面，其次按销量
	rows = list(queryset.order_by('-stock_quantity', '-sold')[:MAX_PRODUCTS])
	if not rows:
		return f'没有找到与「{keyword}」相关的在售商品。'

	lines = []
	for item in rows:
		category = item.types.title if item.types_id else '未分类'
		stock = '有货' if (item.stock_quantity or 0) > 0 else '暂时缺货'
		lines.append(
			f'- {item.sku_title}｜{category}｜￥{item.price}｜{stock}'
			f'｜商品ID {item.id}'
		)
	return '找到以下在售商品：\n' + '\n'.join(lines)


@tool
def search_knowledge_base(question: str) -> str:
	"""
	检索店内的宠物养护知识库，获取喂养、驱虫、洗护等专业资料。

	涉及用量、周期、操作步骤这类需要准确依据的问题，优先用这个工具，
	不要凭记忆回答。

	Args:
		question: 用户的问题原文或核心关键词。
	"""
	try:
		hits = rag.search_knowledge(question, top_k=MAX_KNOWLEDGE_CHUNKS)
	except Exception as exc:  # 检索失败不该让整轮对话崩掉
		logger.warning('知识库检索异常: %s', exc)
		return '知识库暂时不可用，请基于通用常识回答，并提示用户信息可能不完整。'

	if not hits:
		return '知识库中没有相关内容。请如实告知用户店内资料未覆盖该问题。'

	_record_citations([hit['chunk_id'] for hit in hits])

	blocks = []
	for hit in hits:
		blocks.append(f"【{hit['document_title']}】\n{hit['content']}")
	return '知识库检索结果：\n\n' + '\n\n'.join(blocks)


def get_tools() -> list:
	return [search_products, search_knowledge_base]

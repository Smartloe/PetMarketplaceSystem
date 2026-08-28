import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import permissions, status
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConsultMessage, ConsultSession, KnowledgeChunk

logger = logging.getLogger(__name__)

MAX_HISTORY_MESSAGES = 8
# 单条提问的长度上限，避免用超长 prompt 放大上游成本
MAX_QUESTION_CHARS = 2000

# 宠物相关关键词
PET_KEYWORDS = [
	'宠物', '狗', '猫', '鸟', '鱼', '兔子', '仓鼠', '龟', '蛇', '蜥蜴',
	'喂养', '饲养', '训练', '健康', '疾病', '疫苗', '驱虫', '洗澡', '美容',
	'食物', '狗粮', '猫粮', '零食', '玩具', '用品', '笼子', '窝', '牵引绳',
	'宠物店', '宠物医院', '兽医', '品种', '幼犬', '幼猫', '成犬', '成猫',
	'主粮', '猫砂', '尿垫', '益生菌', '羊奶粉', '项圈', '航空箱',
	'pet', 'dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'turtle'
]

# 非宠物相关关键词（需要拒绝的）
NON_PET_KEYWORDS = [
	'编程', '代码', '程序', '软件', '开发', '算法', '数据库', '网站', '系统',
	'政治', '政府', '选举', '党派', '法律', '股票', '投资', '金融', '赚钱',
	'医学', '药物', '治疗', '手术', '人类疾病', '心理学', '哲学', '宗教',
	'programming', 'code', 'software', 'development', 'algorithm', 'database'
]


def _is_pet_related_question(content):
	"""
	粗粒度的话题判断：只用来挡明显跑题的提问。

	白名单优先于黑名单。此前顺序是反的 —— 黑名单先跑，于是只要出现一个
	非宠物词就否决整句，"我的猫咪生病了需要治疗吗"（含"治疗"）、
	"推荐一个宠物喂食系统"（含"系统"）这类正常提问都会被拒。

	需要说明的是：关键词过滤本身挡不住刻意绕过（改写措辞、prompt 注入
	都能穿过），真正约束话题范围的是 agent.py 里的 SYSTEM_PROMPT。
	这里只是省掉一次明显无关的上游调用。
	"""
	if not content:
		return True

	content_lower = content.lower()

	# 先看是否命中宠物关键词；命中就放行，哪怕句子里还夹着别的词
	if any(keyword.lower() in content_lower for keyword in PET_KEYWORDS):
		return True

	# 没有任何宠物线索，才用黑名单挡掉明显属于其他领域的提问
	if any(keyword.lower() in content_lower for keyword in NON_PET_KEYWORDS):
		return False

	# 既无宠物线索也无明显跑题信号（例如打招呼），交给系统提示词处理
	return True


REJECTION_MESSAGE = """很抱歉，我是专门的宠物顾问，只能回答与宠物相关的问题。

我可以帮您解答：
- 主粮、零食的成分与选购
- 驱虫、洗护的周期与用量
- 玩具、牵引、服饰的尺码搭配
- 清洁用品与宠物厕所方案

请问您有什么宠物相关的问题需要咨询吗？"""


def _sanitize_messages(raw_messages):
	"""
	保留最近几轮，并确保每条消息结构完整。

	只接受 user / assistant —— system 由服务端注入。历史里如果允许 system，
	调用方就能塞进自己的指令覆盖顾问的行为边界。
	"""
	if not isinstance(raw_messages, list):
		return []

	cleaned = []
	for item in raw_messages:
		if not isinstance(item, dict):
			continue

		role = item.get('role', 'user')
		content = item.get('content')
		if content is None:
			continue

		role = role if role in {'user', 'assistant'} else 'user'
		cleaned.append({'role': role, 'content': str(content).strip()})

	return cleaned[-MAX_HISTORY_MESSAGES:]


class EventStreamRenderer(BaseRenderer):
	"""
	让 DRF 的内容协商接受 Accept: text/event-stream。

	前端发起流式请求时带的就是这个 Accept 头，而 DRF 默认只配了 JSON 与
	BrowsableAPI，协商失败会直接返回 406 —— 流式请求根本进不到 view。
	实际的 SSE 内容由 StreamingHttpResponse 自己写出，这里不参与渲染。
	"""

	media_type = 'text/event-stream'
	format = 'txt'
	charset = 'utf-8'

	def render(self, data, accepted_media_type=None, renderer_context=None):
		return data


def _sse(payload):
	return f'data: {json.dumps(payload, ensure_ascii=False)}\n\n'


def _stream_response(generator):
	response = StreamingHttpResponse(generator, content_type='text/event-stream')
	response['Cache-Control'] = 'no-cache'
	# 关掉 nginx 的响应缓冲，否则流式内容会被攒着一次性吐出
	response['X-Accel-Buffering'] = 'no'
	# 注意：不要设置 Connection: keep-alive。那是 hop-by-hop 头，WSGI 规范
	# 禁止应用层设置，Django 开发服务器会直接抛 AssertionError，gunicorn
	# 等生产服务器同样拒绝。连接复用由服务器自己管理。
	# CORS 头交给 corsheaders 按白名单添加；手写 '*' 与
	# CORS_ALLOW_CREDENTIALS 组合是非法的，浏览器会拒收。
	return response


def _persist_turn(user, question, answer, cited_chunk_ids, session_id=None):
	"""
	落库这一轮问答。

	写库失败不能影响已经生成好的回答 —— 用户已经等过上游延迟了，
	不该因为持久化问题拿不到结果。
	"""
	try:
		session = None
		if session_id:
			session = ConsultSession.objects.filter(pk=session_id, user=user).first()
		if session is None:
			session = ConsultSession.objects.create(
				user=user, title=question[:60],
			)

		ConsultMessage.objects.create(
			session=session, role=ConsultMessage.ROLE_USER, content=question,
		)
		assistant_message = ConsultMessage.objects.create(
			session=session, role=ConsultMessage.ROLE_ASSISTANT, content=answer,
		)
		if cited_chunk_ids:
			chunks = KnowledgeChunk.objects.filter(pk__in=cited_chunk_ids)
			assistant_message.cited_chunks.set(chunks)
		# 触发 updated_time，让最近会话排在前面
		session.save(update_fields=['updated_time'])
		return session.pk
	except Exception as exc:
		logger.warning('保存 AI 会话失败: %s', exc)
		return session_id


def _build_citations(cited_chunk_ids):
	"""把引用分片整理成前端可展示的来源列表。"""
	if not cited_chunk_ids:
		return []
	rows = (
		KnowledgeChunk.objects
		.filter(pk__in=cited_chunk_ids)
		.select_related('document')
	)
	seen = set()
	citations = []
	for row in rows:
		# 同一份文档命中多个分片时只列一次
		if row.document_id in seen:
			continue
		seen.add(row.document_id)
		citations.append({
			'document_id': row.document_id,
			'title': row.document.title,
			'excerpt': row.content[:120],
		})
	return citations


class AIPetConsultView(APIView):
	"""
	AI 宠物顾问接口。基于 LangGraph 编排，可调用商品搜索与知识库检索。

	需要登录并受限流约束：每次请求都会用服务端的 LONGCAT_API_KEY 去调
	付费上游，匿名且不限速会让任何人都能替我们花钱。
	"""

	permission_classes = (permissions.IsAuthenticated,)
	throttle_scope = 'ai_consult'
	# JSON 放在前面，保持非流式请求的默认行为不变
	renderer_classes = (JSONRenderer, EventStreamRenderer)

	def post(self, request):
		payload = request.data if isinstance(request.data, dict) else {}
		messages = _sanitize_messages(payload.get('messages'))
		question = str(payload.get('question', '')).strip() if payload.get('question') else ''
		stream = payload.get('stream', True)
		session_id = payload.get('session_id')

		# 前端传的是完整历史，最后一条就是本轮提问
		if not question and messages:
			for item in reversed(messages):
				if item['role'] == 'user':
					question = item['content']
					break
			# 历史里去掉本轮提问，避免重复出现在 prompt 里
			if question:
				for index in range(len(messages) - 1, -1, -1):
					if messages[index]['role'] == 'user' and messages[index]['content'] == question:
						messages = messages[:index]
						break

		if not question:
			return Response(
				{'detail': '请提供需要咨询的问题。'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if len(question) > MAX_QUESTION_CHARS or any(
			len(message['content']) > MAX_QUESTION_CHARS for message in messages
		):
			return Response(
				{'detail': f'单条内容请控制在 {MAX_QUESTION_CHARS} 字以内。'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if not _is_pet_related_question(question):
			if stream:
				def rejection_stream():
					yield _sse({'content': REJECTION_MESSAGE})
					yield _sse({'done': True})
				return _stream_response(rejection_stream())
			return Response({'answer': REJECTION_MESSAGE}, status=status.HTTP_200_OK)

		try:
			from .agent import run_agent, stream_agent
		except ImportError as exc:
			logger.error('Agent 依赖缺失: %s', exc)
			return Response(
				{'detail': 'AI 服务暂未就绪，请联系管理员。'},
				status=status.HTTP_503_SERVICE_UNAVAILABLE,
			)

		if stream:
			return _stream_response(
				self._agent_event_stream(stream_agent, messages, question, session_id),
			)

		try:
			result = run_agent(messages, question)
		except RuntimeError as exc:
			# 缺少 API key 之类的配置问题
			logger.error('Agent 配置错误: %s', exc)
			return Response(
				{'detail': 'AI 服务暂未配置，请联系管理员。'},
				status=status.HTTP_503_SERVICE_UNAVAILABLE,
			)
		except Exception as exc:
			logger.exception('Agent 执行失败: %s', exc)
			return Response(
				{'detail': 'AI 服务暂不可用，请稍后再试。'},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		answer = result['answer']
		citations = _build_citations(result.get('cited_chunk_ids'))
		new_session_id = _persist_turn(
			request.user, question, answer,
			result.get('cited_chunk_ids'), session_id,
		)

		return Response(
			{
				'answer': answer,
				'citations': citations,
				'tools_used': result.get('tools_used', []),
				'session_id': new_session_id,
			},
			status=status.HTTP_200_OK,
		)

	def _agent_event_stream(self, stream_agent, messages, question, session_id):
		"""
		把 Agent 的事件流转成 SSE。

		异常必须在生成器内部捕获：StreamingHttpResponse 一旦开始迭代，
		响应头已经发出，这时再抛异常只会让连接中断，前端拿到的是一个
		没有 error 帧的截断流。
		"""
		user = self.request.user
		try:
			for kind, data in stream_agent(messages, question):
				if kind == 'token':
					yield _sse({'content': data})
				elif kind == 'tool_start':
					# 前端据此显示"正在查询商品/知识库"
					yield _sse({'tool': data})
				elif kind == 'final':
					citations = _build_citations(data.get('cited_chunk_ids'))
					new_session_id = _persist_turn(
						user, question, data['answer'],
						data.get('cited_chunk_ids'), session_id,
					)
					yield _sse({
						'done': True,
						'citations': citations,
						'tools_used': data.get('tools_used', []),
						'session_id': new_session_id,
					})
		except RuntimeError as exc:
			logger.error('Agent 配置错误: %s', exc)
			yield _sse({'error': 'AI 服务暂未配置，请联系管理员。'})
		except Exception as exc:
			logger.exception('Agent 流式执行失败: %s', exc)
			yield _sse({'error': 'AI 服务暂不可用，请稍后再试。'})

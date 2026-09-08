import json
import logging
import queue
import threading

from django.db import connections
from django.http import StreamingHttpResponse
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConsultMessage, ConsultSession, KnowledgeChunk

logger = logging.getLogger(__name__)

# 随提问一起发给模型的历史条数上限。前端发送的 history 不含本轮提问，
# 所以这里的 8 就是模型实际能看到的 8 条，不会再被截掉一条。
MAX_HISTORY_MESSAGES = 8
# 单条提问的长度上限，避免用超长 prompt 放大上游成本
MAX_QUESTION_CHARS = 2000
# 会话详情返回的消息条数上限（约 20 轮），避免长会话一次吐出整段历史
MAX_SESSION_MESSAGES = 40
# 会话列表一次返回的条数上限
MAX_SESSION_LIST = 20

# 宠物相关关键词。
#
# 白名单命中即放行（见 _is_pet_related_question），所以一个过宽的词等于
# 一票否决整个黑名单。据此排除了三类词：
#   - 人宠共用的昵称：宝宝、宝贝、主子、小家伙、小可爱
#   - 完全通用的名词/动词：生产、怀孕、散步、健康、食物、用品、窝、推车
#   - 与黑名单条目互为子串的：疾病（黑名单里有"人类疾病"）、刷牙、口臭
# 少了它们不会挡住正常提问 —— 真指向宠物的句子几乎总会同时出现别的宠物词，
# 而两边都无信号的句子本来就会走到最后那条"交给 SYSTEM_PROMPT"的分支。
PET_KEYWORDS = [
	# 正式称呼
	'宠物', '狗', '猫', '鸟', '鱼', '兔子', '仓鼠', '龟', '蛇', '蜥蜴',
	'龙猫', '刺猬', '鹦鹉', '金鱼', '热带鱼', '乌龟', '王八',
	# 口语化称呼
	'狗子', '喵主子', '毛孩子', '崽崽', '崽子', '猫猫', '狗狗',
	'汪星人', '喵星人',
	# 常见品种
	'金毛', '拉布拉多', '泰迪', '比熊', '柯基', '哈士奇', '二哈',
	'英短', '美短', '布偶', '橘猫', '狸花', '暹罗', '加菲',
	# 生活场景
	'喂养', '饲养', '训练', '疫苗', '驱虫', '洗澡', '美容',
	'绝育', '发情', '配种', '繁殖', '哺乳',
	'遛狗', '磨牙', '拆家', '叫唤', '乱尿', '定点',
	# 用品相关
	'狗粮', '猫粮', '零食', '玩具', '笼子', '牵引绳',
	'宠物店', '宠物医院', '兽医', '品种', '幼犬', '幼猫', '成犬', '成猫',
	'主粮', '猫砂', '尿垫', '益生菌', '羊奶粉', '项圈', '航空箱',
	'罐头', '冻干', '生骨肉', '磨牙棒', '猫抓板', '猫爬架',
	'自动喂食器', '饮水机', '宠物背包',
	# 护理相关
	'梳毛', '剪指甲', '掏耳朵', '泪痕',
	'皮肤病', '耳螨', '跳蚤', '蜱虫', '弓形虫',
	# 英文
	'pet', 'dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'turtle',
	'puppy', 'kitten', 'breed',
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


# SSE 心跳间隔（秒）。代理/防火墙通常 60s 断开空闲连接，设 20s 留出余量。
HEARTBEAT_INTERVAL = 20
# 事件队列长度。消费端只是往 socket 写，正常情况下不会积压；给个上限是为了
# 在客户端读得比模型慢时对生产线程施加背压，而不是无限缓冲。
_EVENT_QUEUE_SIZE = 64
# 工作线程结束的哨兵。用独立对象而不是 None，避免和真实事件混淆。
_STREAM_CLOSED = object()


def _pump_agent_events(stream_agent, messages, question, events, stop_event):
	"""
	在工作线程里消费 stream_agent，把事件塞进队列。

	stream_agent 是阻塞的：它在 graph.stream() 里等上游返回，等待期间不会
	产出任何东西。把它放到独立线程，主线程才能在等待期间按固定间隔写心跳
	—— 否则心跳只能在"已经有数据了"之后补发，起不到保活作用。

	异常不往线程外抛（没人 join 得到），统一转成 ('error', 异常) 事件。
	"""
	try:
		for event in stream_agent(messages, question):
			if stop_event.is_set():
				break
			# 用带超时的 put 轮询 stop_event：客户端断开后消费端不再取，
			# 无超时的 put 会让这个线程永久挂在满队列上。
			while not stop_event.is_set():
				try:
					events.put(event, timeout=1)
					break
				except queue.Full:
					continue
	except Exception as exc:
		# 兜住所有异常：线程里抛出去没人接，连接会直接断在半截流上。
		# 具体分类交给消费端的 _describe_agent_error。
		try:
			events.put(('error', exc), timeout=1)
		except queue.Full:
			logger.warning('Agent 线程异常且队列已满，丢弃: %s', exc)
	finally:
		# 工作线程有自己的一套数据库连接（连接是 thread-local 的），
		# 请求结束时 Django 只会关主线程那套，这里必须自己收尾。
		connections.close_all()
		try:
			events.put(_STREAM_CLOSED, timeout=1)
		except queue.Full:
			# 消费端已经走了，没人需要这个哨兵
			pass


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


def _describe_agent_error(exc):
	"""把工作线程里的异常翻译成给用户看的一句话，并留下服务端日志。"""
	if isinstance(exc, RuntimeError):
		# 缺少 API key 之类的配置问题
		logger.error('Agent 配置错误: %s', exc)
		return 'AI 服务暂未配置，请联系管理员。'
	# 已经出了 except 块，得显式把异常实例交给 logging 才有 traceback
	logger.error('Agent 流式执行失败: %s', exc, exc_info=exc)
	return 'AI 服务暂不可用，请稍后再试。'


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

		心跳：stream_agent 是阻塞的，所以它跑在工作线程里，主线程用
		queue.get(timeout=HEARTBEAT_INTERVAL) 等事件。超时就说明这段时间
		上游确实没吐东西，此时写一个 SSE 注释帧保活 —— 这才是"空闲期心跳"。
		把心跳检查写在事件循环体内是无效的：那只会在已经拿到数据之后补发，
		而数据本身早就打破了空闲。
		"""
		user = self.request.user
		events = queue.Queue(maxsize=_EVENT_QUEUE_SIZE)
		stop_event = threading.Event()
		worker = threading.Thread(
			target=_pump_agent_events,
			args=(stream_agent, messages, question, events, stop_event),
			# 进程退出时不因为这个线程卡住
			daemon=True,
			name='ai-consult-stream',
		)
		worker.start()

		try:
			while True:
				try:
					event = events.get(timeout=HEARTBEAT_INTERVAL)
				except queue.Empty:
					# 真正的空闲：这段时间里上游一个 token 都没给
					yield ': heartbeat\n\n'
					continue

				if event is _STREAM_CLOSED:
					break

				kind, data = event

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
				elif kind == 'error':
					yield _sse({'error': _describe_agent_error(data)})
		finally:
			# 客户端断开时 Django 会关掉生成器，走到这里。通知工作线程收手，
			# 否则它会把整轮上游调用跑完（照样计费）再自然结束。
			stop_event.set()


class ConsultSessionPagination(PageNumberPagination):
	"""会话列表分页。页大小固定，不接受客户端指定，避免被要走整张表。"""

	page_size = MAX_SESSION_LIST


class ConsultSessionViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
	"""
	当前用户的 AI 顾问会话：列表、详情、删除。

	归属过滤只写在 get_queryset() 里 —— 这是项目里统一的隔离方式
	（见 CLAUDE.md）。此前 list / detail / delete 是三个 APIView，各自
	手写了一遍 filter(user=request.user)，任何一处漏掉就是越权。
	"""

	permission_classes = (permissions.IsAuthenticated,)
	# 自己的限流桶。不设 throttle_scope 时 ScopedRateThrottle 会无条件放行，
	# 而挂到 ai_consult 上会让浏览历史消耗提问配额。
	throttle_scope = 'ai_sessions'
	# 全局的 PAGE_SIZE 是 6，对侧边栏太碎。分页而不是硬截断：早先是
	# `[:20]` 且两端都没有翻页入口，第 21 个会话之后就永久取不到了。
	pagination_class = ConsultSessionPagination

	def get_queryset(self):
		return ConsultSession.objects.filter(user=self.request.user)

	def list(self, request):
		page = self.paginate_queryset(self.get_queryset())
		data = [
			{
				'id': session.pk,
				'title': str(session),
				'updated_time': session.updated_time.isoformat(),
			}
			for session in page
		]
		return self.get_paginated_response(data)

	def retrieve(self, request, pk=None):
		session = self.get_object()
		# 只取最近若干条：长会话全量返回会让前端一次渲染上百条 markdown，
		# 而它本来就只保留最近几轮用于追问。倒序取再翻回来，避免把整表读进内存。
		recent = list(session.messages.order_by('-created_time', '-id')[:MAX_SESSION_MESSAGES])
		recent.reverse()
		data = [
			{
				'role': msg.role,
				'content': msg.content,
				'created_time': msg.created_time.isoformat(),
			}
			for msg in recent
		]
		return Response(
			{
				'id': session.pk,
				'title': str(session),
				'messages': data,
				# 告诉前端上面还有更早的消息被截断了
				'truncated': session.messages.count() > len(data),
				'created_time': session.created_time.isoformat(),
				'updated_time': session.updated_time.isoformat(),
			},
			status=status.HTTP_200_OK,
		)

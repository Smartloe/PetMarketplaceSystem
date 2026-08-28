import json

from django.db import models


class KnowledgeDocument(models.Model):
	"""
	后台上传的知识库文档。

	原始文件保留在 media/knowledge/ 下，切片后的内容存到 KnowledgeChunk。
	重新上传同一份文档会重建它的分片（见 admin 里的 re-index 动作）。
	"""

	STATUS_PENDING = 'pending'
	STATUS_INDEXING = 'indexing'
	STATUS_READY = 'ready'
	STATUS_FAILED = 'failed'
	STATUS_CHOICES = [
		(STATUS_PENDING, '待处理'),
		(STATUS_INDEXING, '索引中'),
		(STATUS_READY, '已就绪'),
		(STATUS_FAILED, '索引失败'),
	]

	title = models.CharField('文档标题', max_length=200)
	# 分类只用于后台筛选，不参与检索打分
	category = models.CharField('分类', max_length=50, blank=True, default='')
	source_file = models.FileField(
		'源文件', upload_to='knowledge/', blank=True, null=True,
		help_text='支持 .txt / .md。上传后需要执行「重新索引」才会生效。',
	)
	# 允许直接粘贴内容，不上传文件
	raw_text = models.TextField(
		'文本内容', blank=True, default='',
		help_text='可直接粘贴内容；留空则读取上传的源文件。',
	)
	status = models.CharField(
		'状态', max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING,
	)
	# 索引失败时记录原因，便于后台直接看到问题
	error_message = models.TextField('错误信息', blank=True, default='')
	chunk_count = models.PositiveIntegerField('分片数', default=0)
	is_active = models.BooleanField(
		'启用', default=True,
		help_text='停用后该文档不再参与 AI 检索，但分片会保留。',
	)
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	updated_time = models.DateTimeField('更新时间', auto_now=True)

	class Meta:
		verbose_name = '知识库文档'
		verbose_name_plural = '知识库文档'
		ordering = ['-updated_time', '-id']

	def __str__(self):
		return self.title


class KnowledgeChunk(models.Model):
	"""
	文档切片及其向量。

	向量以 JSON 存在 TextField 里，而不是用向量数据库：知识库规模在几千
	分片以内时，取回后用 numpy 算余弦相似度足够快（毫秒级），省掉引入
	pgvector/Milvus 的运维成本。规模上去了再换检索后端，接口不用改。
	"""

	document = models.ForeignKey(
		KnowledgeDocument, on_delete=models.CASCADE,
		related_name='chunks', verbose_name='所属文档',
	)
	content = models.TextField('分片内容')
	position = models.PositiveIntegerField('片序', default=0)
	# 与 EMBEDDING_MODEL 对应。模型不同的分片不能混用，检索时按当前配置过滤。
	embedding_model = models.CharField('向量模型', max_length=100, blank=True, default='')
	embedding_json = models.TextField('向量', blank=True, default='')
	created_time = models.DateTimeField('创建时间', auto_now_add=True)

	class Meta:
		verbose_name = '知识库分片'
		verbose_name_plural = '知识库分片'
		ordering = ['document_id', 'position']
		indexes = [
			models.Index(fields=['document', 'position']),
			models.Index(fields=['embedding_model']),
		]

	def __str__(self):
		return f'{self.document_id}#{self.position}'

	@property
	def embedding(self):
		if not self.embedding_json:
			return None
		try:
			return json.loads(self.embedding_json)
		except (TypeError, ValueError):
			return None

	def set_embedding(self, vector, model_name):
		self.embedding_json = json.dumps(vector)
		self.embedding_model = model_name


class ConsultSession(models.Model):
	"""
	一次 AI 顾问会话。

	会话历史存服务端，而不是完全信任前端回传的 messages —— 前端可以伪造
	任意历史，包括塞进 system 角色的内容来改写指令。
	"""

	user = models.ForeignKey(
		'auth.User', on_delete=models.CASCADE,
		related_name='consult_sessions', verbose_name='用户',
	)
	title = models.CharField('会话标题', max_length=200, blank=True, default='')
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	updated_time = models.DateTimeField('更新时间', auto_now=True)

	class Meta:
		verbose_name = 'AI 会话'
		verbose_name_plural = 'AI 会话'
		ordering = ['-updated_time', '-id']

	def __str__(self):
		return self.title or f'会话 {self.pk}'


class ConsultMessage(models.Model):
	"""会话中的单条消息。"""

	ROLE_USER = 'user'
	ROLE_ASSISTANT = 'assistant'
	ROLE_CHOICES = [(ROLE_USER, '用户'), (ROLE_ASSISTANT, '顾问')]

	session = models.ForeignKey(
		ConsultSession, on_delete=models.CASCADE,
		related_name='messages', verbose_name='所属会话',
	)
	role = models.CharField('角色', max_length=16, choices=ROLE_CHOICES)
	content = models.TextField('内容')
	# 本轮引用到的知识库分片，用于前端展示来源
	cited_chunks = models.ManyToManyField(
		KnowledgeChunk, blank=True, related_name='citations', verbose_name='引用分片',
	)
	created_time = models.DateTimeField('创建时间', auto_now_add=True)

	class Meta:
		verbose_name = 'AI 消息'
		verbose_name_plural = 'AI 消息'
		ordering = ['session_id', 'created_time', 'id']

	def __str__(self):
		return f'{self.get_role_display()}: {self.content[:30]}'

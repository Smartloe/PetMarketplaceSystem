# -*- coding: utf-8 -*-
"""
知识库后台。上传文档后执行「重新索引」即可参与 AI 检索。
"""

from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
	ConsultMessage,
	ConsultSession,
	KnowledgeChunk,
	KnowledgeDocument,
)
from .rag import EmbeddingError, reindex_document


class KnowledgeChunkInline(admin.TabularInline):
	model = KnowledgeChunk
	extra = 0
	can_delete = False
	fields = ('position', 'content_preview', 'embedding_model', 'has_vector')
	readonly_fields = fields
	# 分片可能上百条，默认不展开，避免打开文档页就拖慢后台
	max_num = 0

	def content_preview(self, obj):
		return obj.content[:120] + ('…' if len(obj.content) > 120 else '')

	content_preview.short_description = '内容预览'

	def has_vector(self, obj):
		return bool(obj.embedding_json)

	has_vector.short_description = '已向量化'
	has_vector.boolean = True


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'category', 'status_badge', 'chunk_count', 'is_active', 'updated_time',
	)
	list_filter = ('status', 'is_active', 'category')
	search_fields = ('title', 'raw_text')
	readonly_fields = ('status', 'chunk_count', 'error_message', 'created_time', 'updated_time')
	actions = ('action_reindex', 'action_activate', 'action_deactivate')
	inlines = (KnowledgeChunkInline,)
	fieldsets = (
		('基本信息', {
			'fields': ('title', 'category', 'is_active'),
		}),
		('内容（二选一）', {
			'fields': ('source_file', 'raw_text'),
			'description': '上传 .txt / .md 文件，或直接粘贴文本。保存后请执行「重新索引选中文档」。',
		}),
		('索引状态', {
			'fields': ('status', 'chunk_count', 'error_message', 'created_time', 'updated_time'),
		}),
	)

	def status_badge(self, obj):
		colors = {
			KnowledgeDocument.STATUS_READY: '#2f5d4f',
			KnowledgeDocument.STATUS_FAILED: '#b23a2f',
			KnowledgeDocument.STATUS_INDEXING: '#a8802c',
			KnowledgeDocument.STATUS_PENDING: '#8b8073',
		}
		return format_html(
			'<span style="color:{};font-weight:600">{}</span>',
			colors.get(obj.status, '#8b8073'),
			obj.get_status_display(),
		)

	status_badge.short_description = '状态'

	@admin.action(description='重新索引选中文档')
	def action_reindex(self, request, queryset):
		succeeded = failed = 0
		for document in queryset:
			try:
				count = reindex_document(document)
				if count:
					succeeded += 1
				else:
					failed += 1
			except EmbeddingError as exc:
				failed += 1
				self.message_user(
					request, f'{document.title}：{exc}', level=messages.ERROR,
				)
			except Exception as exc:  # 单份失败不该中断整批
				failed += 1
				self.message_user(
					request, f'{document.title} 索引异常：{exc}', level=messages.ERROR,
				)

		if succeeded:
			self.message_user(request, f'{succeeded} 份文档索引完成。', level=messages.SUCCESS)
		if failed and not succeeded:
			self.message_user(request, '索引失败，请检查错误信息。', level=messages.WARNING)

	@admin.action(description='启用选中文档')
	def action_activate(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(request, f'已启用 {updated} 份文档。')

	@admin.action(description='停用选中文档')
	def action_deactivate(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(request, f'已停用 {updated} 份文档。')


class ConsultMessageInline(admin.TabularInline):
	model = ConsultMessage
	extra = 0
	can_delete = False
	fields = ('role', 'content', 'created_time')
	readonly_fields = fields


@admin.register(ConsultSession)
class ConsultSessionAdmin(admin.ModelAdmin):
	"""会话只读：这里是排查问题用的，不该在后台改写用户的对话记录。"""

	list_display = ('__str__', 'user', 'message_count', 'updated_time')
	list_filter = ('updated_time',)
	search_fields = ('title', 'user__username')
	readonly_fields = ('user', 'title', 'created_time', 'updated_time')
	inlines = (ConsultMessageInline,)

	def has_add_permission(self, request):
		return False

	def message_count(self, obj):
		return obj.messages.count()

	message_count.short_description = '消息数'

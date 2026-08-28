# -*- coding: utf-8 -*-
"""
知识库的切片、向量化与检索。

检索用「取回全部分片 + numpy 算余弦相似度」，没有引入向量数据库。
几千分片以内这样是毫秒级，省掉 pgvector/Milvus 的运维成本；规模上去了
只需要替换 search_knowledge() 的内部实现，调用方不用动。
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.error
import urllib.request

import numpy as np
from django.conf import settings

from .models import KnowledgeChunk, KnowledgeDocument

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_URL = 'https://api.siliconflow.cn/v1/embeddings'
DEFAULT_EMBEDDING_MODEL = 'Qwen/Qwen3-Embedding-0.6B'

# 切片参数。中文按标点断句，再按长度聚合成片。
CHUNK_TARGET_CHARS = 480
CHUNK_OVERLAP_CHARS = 80
# 单次 embedding 请求的分片数上限，避免请求体过大被上游拒绝
EMBED_BATCH_SIZE = 16
# 低于这个相似度就不算命中 —— 否则无论问什么都会返回最像的那条，
# 让模型基于无关内容编造答案。
MIN_SIMILARITY = 0.35


class EmbeddingError(RuntimeError):
	"""向量化失败。调用方需要据此把文档标记成 failed。"""


def get_embedding_model() -> str:
	return os.environ.get('EMBEDDING_MODEL') or DEFAULT_EMBEDDING_MODEL


def _get_api_key() -> str:
	key = os.environ.get('SILICONFLOW_API_KEY', '').strip()
	if not key:
		raise EmbeddingError('未配置 SILICONFLOW_API_KEY，无法向量化知识库。')
	return key


def embed_texts(texts: list[str]) -> list[list[float]]:
	"""
	批量向量化。返回顺序与入参一致。

	用标准库发请求而不是 openai SDK：这里只需要一个 POST，少一层依赖，
	也避免 SDK 版本升级改变行为。
	"""
	if not texts:
		return []

	api_key = _get_api_key()
	model = get_embedding_model()
	url = os.environ.get('EMBEDDING_API_URL') or DEFAULT_EMBEDDING_URL
	vectors: list[list[float]] = []

	for start in range(0, len(texts), EMBED_BATCH_SIZE):
		batch = texts[start:start + EMBED_BATCH_SIZE]
		payload = json.dumps({'input': batch, 'model': model}).encode('utf-8')
		request = urllib.request.Request(
			url,
			data=payload,
			headers={
				'Authorization': f'Bearer {api_key}',
				'Content-Type': 'application/json',
			},
		)
		try:
			with urllib.request.urlopen(request, timeout=60) as response:
				body = json.load(response)
		except urllib.error.HTTPError as exc:
			detail = exc.read().decode('utf-8', errors='replace')[:200]
			raise EmbeddingError(f'向量化服务返回 {exc.code}: {detail}') from exc
		except (urllib.error.URLError, TimeoutError) as exc:
			raise EmbeddingError(f'无法连接向量化服务: {exc}') from exc

		data = body.get('data')
		if not isinstance(data, list) or len(data) != len(batch):
			raise EmbeddingError('向量化服务返回的数据条数与请求不一致。')

		# 上游不保证顺序，按 index 字段回排
		ordered = sorted(data, key=lambda item: item.get('index', 0))
		vectors.extend(item['embedding'] for item in ordered)

	return vectors


def split_text(text: str) -> list[str]:
	"""
	按中文标点断句后聚合成片，带重叠。

	不用 langchain 的 RecursiveCharacterTextSplitter：它按字符硬切，
	中文容易在句子中间断开，检索出来的片段读着不完整。
	"""
	normalized = re.sub(r'\r\n?', '\n', text or '').strip()
	if not normalized:
		return []

	# 在句末标点后切开，保留标点本身
	sentences = re.split(r'(?<=[。！？!?；;\n])', normalized)
	sentences = [s.strip() for s in sentences if s.strip()]

	chunks: list[str] = []
	current = ''
	for sentence in sentences:
		# 单句就超长的，硬切开，避免产生一个巨大分片
		while len(sentence) > CHUNK_TARGET_CHARS:
			if current:
				chunks.append(current)
				current = ''
			chunks.append(sentence[:CHUNK_TARGET_CHARS])
			sentence = sentence[CHUNK_TARGET_CHARS:]

		if len(current) + len(sentence) <= CHUNK_TARGET_CHARS:
			current += sentence
			continue

		chunks.append(current)
		# 带上一片的尾部做重叠，避免答案正好落在切口上
		tail = current[-CHUNK_OVERLAP_CHARS:] if CHUNK_OVERLAP_CHARS else ''
		current = tail + sentence

	if current.strip():
		chunks.append(current)

	return [c.strip() for c in chunks if c.strip()]


def read_document_text(document: KnowledgeDocument) -> str:
	"""取文档正文：优先 raw_text，否则读上传的文件。"""
	if document.raw_text.strip():
		return document.raw_text

	if not document.source_file:
		return ''

	try:
		document.source_file.open('rb')
		data = document.source_file.read()
	finally:
		document.source_file.close()

	for encoding in ('utf-8', 'utf-8-sig', 'gb18030'):
		try:
			return data.decode(encoding)
		except UnicodeDecodeError:
			continue
	# 兜底：不因为个别坏字节就整份文档失败
	return data.decode('utf-8', errors='replace')


def reindex_document(document: KnowledgeDocument) -> int:
	"""
	重建一份文档的分片与向量。返回分片数。

	整个过程放在一次事务里：失败时不留下半套分片，否则检索会命中残缺内容。
	"""
	from django.db import transaction

	text = read_document_text(document)
	chunks = split_text(text)

	if not chunks:
		with transaction.atomic():
			document.chunks.all().delete()
			document.chunk_count = 0
			document.status = KnowledgeDocument.STATUS_FAILED
			document.error_message = '文档内容为空，没有可索引的文本。'
			document.save(update_fields=['chunk_count', 'status', 'error_message', 'updated_time'])
		return 0

	document.status = KnowledgeDocument.STATUS_INDEXING
	document.save(update_fields=['status', 'updated_time'])

	try:
		vectors = embed_texts(chunks)
	except EmbeddingError as exc:
		document.status = KnowledgeDocument.STATUS_FAILED
		document.error_message = str(exc)
		document.save(update_fields=['status', 'error_message', 'updated_time'])
		logger.error('知识库索引失败 doc=%s: %s', document.pk, exc)
		raise

	model = get_embedding_model()
	with transaction.atomic():
		document.chunks.all().delete()
		rows = []
		for position, (content, vector) in enumerate(zip(chunks, vectors)):
			row = KnowledgeChunk(document=document, content=content, position=position)
			row.set_embedding(vector, model)
			rows.append(row)
		KnowledgeChunk.objects.bulk_create(rows, batch_size=200)

		document.chunk_count = len(rows)
		document.status = KnowledgeDocument.STATUS_READY
		document.error_message = ''
		document.save(update_fields=['chunk_count', 'status', 'error_message', 'updated_time'])

	return len(rows)


def search_knowledge(query: str, top_k: int = 4) -> list[dict]:
	"""
	检索最相关的分片。

	只取当前 EMBEDDING_MODEL 产出的向量：换模型后旧向量落在不同的向量
	空间，混在一起算相似度得到的是噪声。
	"""
	query = (query or '').strip()
	if not query:
		return []

	model = get_embedding_model()
	rows = list(
		KnowledgeChunk.objects
		.filter(
			document__is_active=True,
			document__status=KnowledgeDocument.STATUS_READY,
			embedding_model=model,
		)
		.exclude(embedding_json='')
		.select_related('document')
		.only('id', 'content', 'embedding_json', 'document__title', 'document__id')
	)
	if not rows:
		return []

	try:
		query_vector = np.asarray(embed_texts([query])[0], dtype=np.float32)
	except (EmbeddingError, IndexError) as exc:
		logger.warning('检索时向量化失败: %s', exc)
		return []

	matrix = []
	usable = []
	for row in rows:
		vector = row.embedding
		# 维度不一致的是换模型后的残留，跳过而不是让 numpy 报错
		if vector and len(vector) == query_vector.shape[0]:
			matrix.append(vector)
			usable.append(row)
	if not usable:
		return []

	doc_matrix = np.asarray(matrix, dtype=np.float32)
	norms = np.linalg.norm(doc_matrix, axis=1) * np.linalg.norm(query_vector)
	# 全零向量会让分母为 0，置 1 避免 nan
	norms[norms == 0] = 1.0
	scores = doc_matrix @ query_vector / norms

	order = np.argsort(-scores)[:top_k]
	results = []
	for index in order:
		score = float(scores[index])
		if score < MIN_SIMILARITY:
			continue
		row = usable[index]
		results.append({
			'chunk_id': row.id,
			'content': row.content,
			'score': round(score, 4),
			'document_id': row.document_id,
			'document_title': row.document.title,
		})
	return results


def get_settings_summary() -> dict:
	"""给后台展示当前 RAG 配置，便于确认 key 是否配好。"""
	return {
		'model': get_embedding_model(),
		'api_key_configured': bool(os.environ.get('SILICONFLOW_API_KEY', '').strip()),
		'dimension': os.environ.get('EMBEDDING_DIM', '未设置'),
		'debug': settings.DEBUG,
	}

import logging
import os

import requests
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

LONGCAT_API_URL = "https://api.longcat.chat/openai/v1/chat/completions"
DEFAULT_LONGCAT_MODEL = "LongCat-Flash-Chat"
MAX_HISTORY_MESSAGES = 8

logger = logging.getLogger(__name__)


def _sanitize_messages(raw_messages):
	"""
	Keep the last few turns and ensure every message has the required shape.
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

		role = role if role in {'user', 'assistant', 'system'} else 'user'
		cleaned.append({
			'role': role,
			'content': str(content).strip()
		})

	return cleaned[-MAX_HISTORY_MESSAGES:]


class AIPetConsultView(APIView):
	"""
	Simple proxy endpoint that hides the third-party API key from the frontend.
	"""
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request):
		payload = request.data if isinstance(request.data, dict) else {}
		messages = _sanitize_messages(payload.get('messages'))
		question = str(payload.get('question', '')).strip() if payload.get('question') else ''

		if not messages:
			if question:
				messages = [{'role': 'user', 'content': question}]
			else:
				return Response(
					{'detail': '请提供需要咨询的问题。'},
					status=status.HTTP_400_BAD_REQUEST
				)

		api_key = os.environ.get('LONGCAT_API_KEY')
		if not api_key:
			logger.error("LONGCAT_API_KEY is not configured.")
			return Response(
				{'detail': 'AI 服务暂未配置，请联系管理员。'},
				status=status.HTTP_503_SERVICE_UNAVAILABLE
			)

		request_body = {
			'model': payload.get('model', DEFAULT_LONGCAT_MODEL),
			'messages': messages,
			'max_tokens': payload.get('max_tokens', 800),
			'temperature': payload.get('temperature', 0.7)
		}
		headers = {
			'Authorization': f'Bearer {api_key}',
			'Content-Type': 'application/json'
		}

		try:
			response = requests.post(
				os.environ.get('LONGCAT_API_URL', LONGCAT_API_URL),
				headers=headers,
				json=request_body,
				timeout=20
			)
			response.raise_for_status()
		except requests.Timeout:
			logger.warning("LongCat API timed out.")
			return Response(
				{'detail': 'AI 服务响应超时，请稍后再试。'},
				status=status.HTTP_504_GATEWAY_TIMEOUT
			)
		except requests.RequestException as exc:
			logger.error("LongCat API error: %s", exc)
			return Response(
				{'detail': 'AI 服务暂不可用，请稍后再试。'},
				status=status.HTTP_502_BAD_GATEWAY
			)

		data = response.json()
		choices = data.get('choices') or []
		answer = None
		if choices:
			first_choice = choices[0] or {}
			message = first_choice.get('message') or {}
			answer = message.get('content') or first_choice.get('text')

		if not answer:
			answer = '抱歉，我暂时无法回答这个问题。'

		return Response(
			{
				'answer': answer.strip(),
				'usage': data.get('usage', {}),
			},
			status=status.HTTP_200_OK
		)

# Create your views here.

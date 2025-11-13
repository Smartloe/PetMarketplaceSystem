import json
import logging
import os
import re

import requests
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

LONGCAT_API_URL = "https://api.longcat.chat/openai/v1/chat/completions"
DEFAULT_LONGCAT_MODEL = "LongCat-Flash-Chat"
MAX_HISTORY_MESSAGES = 8

logger = logging.getLogger(__name__)

# 宠物相关关键词
PET_KEYWORDS = [
    '宠物', '狗', '猫', '鸟', '鱼', '兔子', '仓鼠', '龟', '蛇', '蜥蜴',
    '喂养', '饲养', '训练', '健康', '疾病', '疫苗', '驱虫', '洗澡', '美容',
    '食物', '狗粮', '猫粮', '零食', '玩具', '用品', '笼子', '窝', '牵引绳',
    '宠物店', '宠物医院', '兽医', '品种', '幼犬', '幼猫', '成犬', '成猫',
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
    检查问题是否与宠物相关
    """
    if not content:
        return True
        
    content_lower = content.lower()
    
    # 检查是否包含非宠物关键词
    for keyword in NON_PET_KEYWORDS:
        if keyword.lower() in content_lower:
            return False
    
    # 检查是否包含宠物关键词
    for keyword in PET_KEYWORDS:
        if keyword.lower() in content_lower:
            return True
    
    # 如果没有明确的关键词，但问题很短，可能是打招呼
    if len(content.strip()) < 10:
        return True
    
    # 默认允许，避免过度限制
    return True

def _get_pet_system_prompt():
    """
    获取宠物顾问的系统提示词
    """
    return """你是吉祥宠物商城的专业AI宠物顾问，专门为用户提供宠物相关的咨询服务。

你的职责：
1. 回答关于宠物饲养、健康、训练、用品选择等问题
2. 推荐适合的宠物食品、玩具、用品等商品
3. 提供宠物护理、美容、医疗等专业建议
4. 帮助用户选择适合的宠物品种

重要限制：
- 只回答宠物相关的问题
- 拒绝回答编程、政治、金融、医学等非宠物领域的问题
- 如果用户问非宠物问题，礼貌地引导他们询问宠物相关内容

回答风格：
- 专业、友好、耐心
- 使用简洁明了的语言
- 适当使用emoji增加亲和力
- 支持markdown格式输出

请始终记住你是宠物领域的专家顾问！"""


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

def _prepare_messages_with_system_prompt(messages):
    """
    在消息列表前添加系统提示词
    """
    system_message = {
        'role': 'system',
        'content': _get_pet_system_prompt()
    }
    
    # 检查是否已有系统消息
    has_system = any(msg.get('role') == 'system' for msg in messages)
    
    if not has_system:
        return [system_message] + messages
    
    return messages

def _generate_streaming_response(api_key, request_body):
    """
    生成流式响应
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 启用流式输出
    request_body['stream'] = True
    
    try:
        response = requests.post(
            os.environ.get('LONGCAT_API_URL', LONGCAT_API_URL),
            headers=headers,
            json=request_body,
            stream=True,
            timeout=30
        )
        response.raise_for_status()
        
        def event_stream():
            try:
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # 移除 'data: ' 前缀
                            
                            if data_str.strip() == '[DONE]':
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                            
                            try:
                                data = json.loads(data_str)
                                choices = data.get('choices', [])
                                if choices:
                                    delta = choices[0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"data: {json.dumps({'error': '流式传输出现错误'})}\n\n"
        
        return event_stream()
        
    except requests.Timeout:
        logger.warning("LongCat API timed out.")
        def error_stream():
            yield f"data: {json.dumps({'error': 'AI 服务响应超时，请稍后再试。'})}\n\n"
        return error_stream()
        
    except requests.RequestException as exc:
        logger.error("LongCat API error: %s", exc)
        def error_stream():
            yield f"data: {json.dumps({'error': 'AI 服务暂不可用，请稍后再试。'})}\n\n"
        return error_stream()


class AIPetConsultView(APIView):
    """
    AI宠物顾问接口，支持流式输出和内容过滤
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        payload = request.data if isinstance(request.data, dict) else {}
        messages = _sanitize_messages(payload.get('messages'))
        question = str(payload.get('question', '')).strip() if payload.get('question') else ''
        stream = payload.get('stream', True)  # 默认启用流式输出

        if not messages:
            if question:
                messages = [{'role': 'user', 'content': question}]
            else:
                return Response(
                    {'detail': '请提供需要咨询的问题。'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 检查最新用户消息是否与宠物相关
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        if user_messages:
            latest_question = user_messages[-1].get('content', '')
            if not _is_pet_related_question(latest_question):
                rejection_message = """很抱歉，我是专门的宠物顾问，只能回答与宠物相关的问题。🐾

我可以帮您解答：
- 🐕 宠物饲养和护理问题
- 🐱 宠物健康和医疗咨询  
- 🎾 宠物用品选择建议
- 🏠 宠物训练和行为问题
- 🍖 宠物食品和营养搭配

请问您有什么宠物相关的问题需要咨询吗？"""
                
                if stream:
                    def rejection_stream():
                        yield f"data: {json.dumps({'content': rejection_message})}\n\n"
                        yield f"data: {json.dumps({'done': True})}\n\n"
                    
                    response = StreamingHttpResponse(
                        rejection_stream(),
                        content_type='text/event-stream'
                    )
                    response['Cache-Control'] = 'no-cache'
                    response['Connection'] = 'keep-alive'
                    response['Access-Control-Allow-Origin'] = '*'
                    return response
                else:
                    return Response({'answer': rejection_message}, status=status.HTTP_200_OK)

        api_key = os.environ.get('LONGCAT_API_KEY')
        if not api_key:
            logger.error("LONGCAT_API_KEY is not configured.")
            return Response(
                {'detail': 'AI 服务暂未配置，请联系管理员。'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 添加系统提示词
        messages = _prepare_messages_with_system_prompt(messages)

        request_body = {
            'model': payload.get('model', DEFAULT_LONGCAT_MODEL),
            'messages': messages,
            'max_tokens': payload.get('max_tokens', 1200),
            'temperature': payload.get('temperature', 0.7)
        }

        if stream:
            # 返回流式响应
            event_stream = _generate_streaming_response(api_key, request_body)
            response = StreamingHttpResponse(
                event_stream,
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            response['Connection'] = 'keep-alive'
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            # 返回普通响应（兼容旧版本）
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

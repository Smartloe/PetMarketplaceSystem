import json
import logging
import os

import requests
from django.http import StreamingHttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

LONGCAT_API_URL = "https://api.longcat.chat/openai/v1/chat/completions"
DEFAULT_LONGCAT_MODEL = "LongCat-Flash-Chat"
MAX_HISTORY_MESSAGES = 8

# 上游调用的参数由服务端固定，不接受请求体覆盖 —— 否则任何调用方
# 都能自己挑模型、把 max_tokens 拉满，用我们的 API key 计费。
LONGCAT_MAX_TOKENS = 1200
LONGCAT_TEMPERATURE = 0.7
# 单条提问的长度上限，避免用超长 prompt 放大上游成本
MAX_QUESTION_CHARS = 2000

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
    粗粒度的话题判断：只用来挡明显跑题的提问。

    白名单优先于黑名单。此前顺序是反的 —— 黑名单先跑，于是只要出现一个
    非宠物词就否决整句，"我的猫咪生病了需要治疗吗"（含"治疗"）、
    "推荐一个宠物喂食系统"（含"系统"）这类正常提问都会被拒。

    需要说明的是：关键词过滤本身挡不住刻意绕过（改写措辞、prompt 注入
    都能穿过），真正约束话题范围的是 _get_pet_system_prompt() 里的系统
    提示词。这里只是省掉一次明显无关的上游调用。
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

    需要登录并受限流约束：每次请求都会用服务端的 LONGCAT_API_KEY 去调
    付费上游，匿名且不限速会让任何人都能替我们花钱。
    """
    permission_classes = (permissions.IsAuthenticated,)
    throttle_scope = 'ai_consult'

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

        if any(len(message['content']) > MAX_QUESTION_CHARS for message in messages):
            return Response(
                {'detail': f'单条内容请控制在 {MAX_QUESTION_CHARS} 字以内。'},
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
                    # CORS 头交给 corsheaders 按白名单添加；手写 '*' 与
                    # CORS_ALLOW_CREDENTIALS 组合是非法的，浏览器会拒收。
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

        # 模型与生成参数一律由服务端决定，忽略请求体里的同名字段
        request_body = {
            'model': DEFAULT_LONGCAT_MODEL,
            'messages': messages,
            'max_tokens': LONGCAT_MAX_TOKENS,
            'temperature': LONGCAT_TEMPERATURE,
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

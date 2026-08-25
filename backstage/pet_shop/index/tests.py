"""
AI pet advisor endpoint: access control and topic filtering.
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from index.views import _is_pet_related_question


class TopicFilterTests(APITestCase):
    """
    The whitelist must win over the blacklist.

    The original order ran the blacklist first, so a single off-topic word
    vetoed the whole question and legitimate pet questions were rejected.
    """

    def test_pet_questions_survive_an_incidental_blacklist_word(self):
        for question in (
            '我的猫咪生病了需要治疗吗',   # 含"治疗"
            '请推荐一个宠物喂食系统',      # 含"系统"
            '我家猫的心理学问题',          # 含"心理学"
            '狗狗得了皮肤疾病怎么办',      # 含"疾病"
        ):
            with self.subTest(question=question):
                self.assertTrue(_is_pet_related_question(question))

    def test_clearly_off_topic_questions_are_rejected(self):
        for question in ('给我写一段Python代码', '帮我分析一下股票投资'):
            with self.subTest(question=question):
                self.assertFalse(_is_pet_related_question(question))

    def test_greeting_is_allowed(self):
        self.assertTrue(_is_pet_related_question('你好'))

    def test_empty_input_is_allowed(self):
        self.assertTrue(_is_pet_related_question(''))


class AIConsultAccessTests(APITestCase):
    """The endpoint spends money on every call, so it must require a login."""

    def test_anonymous_request_is_rejected(self):
        response = self.client.post(
            '/api/ai/consult/',
            {'question': '猫咪怎么养'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_request_without_question_is_a_400(self):
        """Authenticated but empty: validated before any upstream call."""
        user = User.objects.create_user('dave', 'd@example.com', 'pw-dave-123')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/ai/consult/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlong_question_is_rejected_before_calling_upstream(self):
        user = User.objects.create_user('erin', 'e@example.com', 'pw-erin-123')
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/api/ai/consult/',
            {'question': '猫' * 2001},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

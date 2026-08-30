"""
Authentication tests: JWT login flow, captcha handling, CSRF restoration.
"""
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase


class CaptchaTests(APITestCase):
    def tearDown(self):
        cache.clear()

    def test_captcha_response_does_not_leak_the_answer(self):
        """The image is returned; the answer stays server-side in the cache."""
        response = self.client.get('/api/accounts/captcha/', {'username': 'someone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('img', response.data)
        self.assertNotIn('code', response.data)

    def test_captcha_requires_username(self):
        response = self.client.get('/api/accounts/captcha/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JwtLoginTests(APITestCase):
    def setUp(self):
        self.password = 'correct-horse-battery'
        self.user = User.objects.create_user('carol', 'c@example.com', self.password)

    def tearDown(self):
        cache.clear()

    def _issue_captcha(self, username='carol'):
        """Drive the real captcha endpoint, then read the answer from cache."""
        self.client.get('/api/accounts/captcha/', {'username': username})
        return cache.get(f'verify_code_{username}')

    def test_login_returns_jwt_pair(self):
        code = self._issue_captcha()
        response = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': code,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_token_authenticates_a_protected_endpoint(self):
        code = self._issue_captcha()
        access = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': code,
        }).data['access']

        # A fresh client with no session cookie, authenticating by Bearer alone.
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get('/api/trade/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint_rejects_missing_token(self):
        response = self.client.get('/api/trade/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_yields_a_new_access_token(self):
        code = self._issue_captcha()
        refresh = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': code,
        }).data['refresh']

        response = self.client.post('/api/accounts/token/refresh/', {'refresh': refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_captcha_is_single_use(self):
        """Replaying a captcha must fail, so it can't be reused to brute-force."""
        code = self._issue_captcha()
        first = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': code,
        })
        self.assertEqual(first.status_code, status.HTTP_200_OK)

        second = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': code,
        })
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_captcha_is_rejected(self):
        self._issue_captcha()
        response = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': self.password, 'code': 'ZZZZZ',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_password_is_rejected(self):
        code = self._issue_captcha()
        response = self.client.post('/api/accounts/login/', {
            'username': 'carol', 'password': 'not-the-password', 'code': code,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterPasswordPolicyTests(APITestCase):
    """API 注册必须过 AUTH_PASSWORD_VALIDATORS，弱口令不能入库。"""

    def _register(self, password):
        return self.client.post("/api/accounts/register/", {
            "username": "newuser1", "email": "newuser1@example.com",
            "password": password, "password2": password,
        }, format="json")

    def test_weak_passwords_are_rejected(self):
        # 依次命中：最小长度、常见口令、与用户名相似
        for weak in ("1234", "password", "newuser1234"):
            with self.subTest(password=weak):
                response = self._register(weak)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="newuser1").exists())

    def test_strong_password_is_accepted(self):
        response = self._register("horse-battery-staple-9")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser1").exists())

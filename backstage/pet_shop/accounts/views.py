# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from .utils.code import check_code
from django.core.cache import cache
import base64
from io import BytesIO


class RegisterView(APIView):
	"""
	用户注册视图
	"""
	# 取消所有认证
	authentication_classes = []
	permission_classes = []

	def post(self, request):
		"""
		处理用户注册请求
		"""
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response(
				{
					"status": status.HTTP_200_OK,
					"message": "用户注册成功",
					"details": {
						'username': user.username,
						'email': user.email,
					}
				},
				status=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
	"""
	用户登录视图
	"""
	# 取消所有认证
	authentication_classes = []
	permission_classes = []

	def post(self, request):
		"""
		处理用户登录请求
		"""
		serializer = LoginSerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.validated_data['username']
			password = serializer.validated_data['password']
			code = serializer.validated_data['code']
			# 从缓存中获取验证码
			cached_code = cache.get(f'verify_code_{username}')
			if cached_code and cached_code == code:
				user = authenticate(request, username=username, password=password)
				if user is not None:
					# 使用django自带的login函数进行登录
					login(request, user)
					print("登录后的", request.user)
					return Response(
						{
							"status": status.HTTP_200_OK,
							"message": "用户登录成功",
						},
						status=status.HTTP_200_OK
					)
				else:
					return Response({'error': '无效的用户名或密码'}, status=status.HTTP_401_UNAUTHORIZED)
			else:
				return Response({'error': '验证码无效'}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
	"""
	用户登出视图
	"""

	def post(self, request):
		"""
		处理用户登出请求
		"""
		# 使用django自带的logout函数进行登出
		logout(request)
		return Response(
			{
				"status": status.HTTP_200_OK,
				"message": "用户登出成功",
			},
			status=status.HTTP_200_OK
		)


class CaptchaView(APIView):
	"""
	验证码视图
	"""
	# 取消所有认证
	authentication_classes = []
	permission_classes = []

	def get(self, request):
		"""
		生成并返回验证码图片
		"""
		username = request.GET.get('username')
		if username:
			# 生成验证码图片和文本
			img, code = check_code()
			# 将验证码文本存储到缓存中,有效期60秒
			cache.set(f'verify_code_{username}', code, 60)

			# 将验证码图片转换为Base64编码的字符串返回
			buffer = BytesIO()
			img.save(buffer, format='JPEG')
			img_str = base64.b64encode(buffer.getvalue()).decode()

			return Response({'code': code, 'img': img_str}, content_type='application/json')
		return Response({'error': '请提供用户名'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
	"""
	用户信息视图集
	"""
	serializer_class = UserProfileSerializer
	permission_classes = [IsOwnerOrReadOnly, IsAdminUser]

	def get_queryset(self):
		"""
		只返回当前登录用户的用户信息
		"""
		return UserProfile.objects.filter(username=self.request.user)

	def perform_create(self, serializer):
		"""
		创建用户信息时,设置当前登录用户为关联的用户
		"""
		serializer.save(username=self.request.user)

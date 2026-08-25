from django.contrib.auth import authenticate, logout
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
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

	成功后返回一对 JWT（access / refresh）。前端只保存这两个 token，
	不再保存明文密码 —— 早期版本让前端把密码写进 localStorage 并对
	每个请求做 Basic Auth，任何一次 XSS 都会直接泄露可复用的凭据。
	"""
	# 取消所有认证
	authentication_classes = []
	permission_classes = []
	throttle_scope = 'login'

	def post(self, request):
		"""
		处理用户登录请求
		"""
		serializer = LoginSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		username = serializer.validated_data['username']
		password = serializer.validated_data['password']
		code = serializer.validated_data['code']

		# 从缓存中获取验证码。一次性使用：无论成败都删掉，
		# 避免同一个验证码被反复用来撞密码。
		cache_key = f'verify_code_{username}'
		cached_code = cache.get(cache_key)
		cache.delete(cache_key)

		if not cached_code or cached_code.lower() != code.lower():
			return Response({'error': '验证码无效'}, status=status.HTTP_400_BAD_REQUEST)

		user = authenticate(request, username=username, password=password)
		if user is None:
			return Response({'error': '无效的用户名或密码'}, status=status.HTTP_401_UNAUTHORIZED)

		last_login = user.last_login
		refresh = RefreshToken.for_user(user)
		# for_user 会更新 last_login，这里回传本次登录之前的值，
		# 保持与旧接口一致的语义。
		return Response(
			{
				"status": status.HTTP_200_OK,
				"message": "用户登录成功",
				"id": user.id,
				"username": user.username,
				"email": user.email,
				"last_login": last_login,
				"access": str(refresh.access_token),
				"refresh": str(refresh),
			},
			status=status.HTTP_200_OK
		)


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

	只返回图片。答案留在服务端缓存里，由 LoginView 校验 ——
	早期版本把 code 一起放进响应体，等于把答案交给调用方，
	对脚本没有任何拦截作用。
	"""
	# 取消所有认证
	authentication_classes = []
	permission_classes = []
	throttle_scope = 'captcha'

	def get(self, request):
		"""
		生成并返回验证码图片
		"""
		username = request.GET.get('username')
		if not username:
			return Response({'error': '请提供用户名'}, status=status.HTTP_400_BAD_REQUEST)

		# 生成验证码图片和文本
		img, code = check_code()
		# 将验证码文本存储到缓存中,有效期60秒
		cache.set(f'verify_code_{username}', code, 60)

		# 将验证码图片转换为Base64编码的字符串返回
		buffer = BytesIO()
		img.save(buffer, format='JPEG')
		img_str = base64.b64encode(buffer.getvalue()).decode()

		return Response({'img': img_str}, content_type='application/json')


class UserProfileViewSet(viewsets.ModelViewSet):
	"""
	用户信息视图集
	"""
	serializer_class = UserProfileSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def get_queryset(self):
		"""
		只返回当前登录用户的用户信息

		这里刻意不做 get_or_create —— get_queryset 会在每次 GET 时调用，
		在读路径上写库会让并发的列表请求互相竞争。缺失的档案改由
		list() 惰性补齐。
		"""
		user = self.request.user
		if not user or not user.is_authenticated:
			return UserProfile.objects.none()
		return UserProfile.objects.filter(username=user)

	def list(self, request, *args, **kwargs):
		"""
		首次访问个人中心时补齐档案，避免新用户看到空列表。
		"""
		user = request.user
		if user and user.is_authenticated:
			UserProfile.objects.get_or_create(username=user)
		return super().list(request, *args, **kwargs)

	def perform_create(self, serializer):
		"""
		创建用户信息时,设置当前登录用户为关联的用户
		"""
		serializer.save(username=self.request.user)


class AvatarUploadView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		file_obj = request.FILES.get('avatar')
		if not file_obj:
			return Response({'detail': '请上传头像文件'}, status=status.HTTP_400_BAD_REQUEST)

		profile, _ = UserProfile.objects.get_or_create(username=request.user)
		profile.avatar = file_obj
		profile.save(update_fields=['avatar'])

		return Response({
			'avatar': request.build_absolute_uri(profile.avatar.url) if profile.avatar else ''
		}, status=status.HTTP_200_OK)

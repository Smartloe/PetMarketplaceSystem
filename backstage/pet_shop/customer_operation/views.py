from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from .permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt  # 免除csrf认证


class UserFavViewSet(viewsets.ModelViewSet):
	"""
	用户收藏视图集
	"""
	serializer_class = UserFavSerializer
	permission_classes = [permissions.IsAuthenticated]

	@csrf_exempt
	def get_queryset(self):
		"""
		只返回当前登录用户的收藏记录
		"""
		return UserFav.objects.filter(user=self.request.user)


class UserLeavingMessageViewSet(viewsets.ModelViewSet):
	"""
	用户留言视图集
	"""
	serializer_class = UserLeavingMessageSerializer
	permission_classes = [permissions.IsAuthenticated]

	@csrf_exempt
	def get_queryset(self):
		"""
		只返回当前登录用户的留言记录
		"""
		return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
	"""
	用户地址视图集
	"""
	serializer_class = UserAddressSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

	@csrf_exempt
	def get_queryset(self):
		"""
		只返回当前登录用户的地址记录
		"""
		return UserAddress.objects.filter(user=self.request.user)


class UserCommentViewSet(viewsets.ModelViewSet):
	"""
	用户评论视图集
	"""
	queryset = UserComment.objects.all()
	serializer_class = UserCommentSerializer

	@csrf_exempt
	def get_permissions(self):
		"""
		实例化并返回此视图所需的权限列表。
		"""
		# 对于安全的方法（如读取操作），允许任何用户访问
		if self.action in ['list', 'retrieve']:
			permission_classes = [permissions.AllowAny]
		else:  # 对于写入操作，仅允许已认证的用户访问
			permission_classes = [permissions.IsAuthenticated]
		return [permission() for permission in permission_classes]

	@csrf_exempt
	def perform_create(self, serializer):
		# 自动设置评论的用户为当前登录用户
		serializer.save(user=self.request.user)

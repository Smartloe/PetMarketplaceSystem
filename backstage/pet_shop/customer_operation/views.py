from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from .permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt  # 免除csrf认证
from pet_shop.regions import get_region_helper


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


class UserCommentViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	用户评论视图集（只读）。
	评论的创建只随 trade 的确认收货评价端点发生——此前这里的通用
	create 可以绕过“确认收货后才能评价”的校验；未通过审核
	（is_show=False）的评论对非管理员不可见。
	"""
	serializer_class = UserCommentSerializer
	permission_classes = [permissions.AllowAny]

	def get_queryset(self):
		user = self.request.user
		if user.is_authenticated and user.is_staff:
			return UserComment.objects.all()
		return UserComment.objects.filter(is_show=True)


class RegionListView(APIView):
	permission_classes = [permissions.AllowAny]
	authentication_classes = []

	def get(self, request):
		options = get_region_helper().get_cascader()
		return Response(options)

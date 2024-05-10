from rest_framework import viewsets
from .models import OrderInfos, OrderGoods, ShoppingCart
from .serializers import OrderInfosSerializer, OrderGoodsSerializer, ShoppingCartSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class OrderInfosViewSet(viewsets.ModelViewSet):
	queryset = OrderInfos.objects.all()
	serializer_class = OrderInfosSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

	def get_queryset(self):
		"""
		只返回当前登录用户的订单记录
		"""
		return OrderInfos.objects.filter(user=self.request.user)


class OrderGoodsViewSet(viewsets.ModelViewSet):
	queryset = OrderGoods.objects.all()
	serializer_class = OrderGoodsSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

	def get_queryset(self):
		"""
		只返回当前登录用户的订单商品记录
		"""
		return OrderGoods.objects.filter(order__user=self.request.user)


class ShoppingCartViewSet(viewsets.ModelViewSet):
	queryset = ShoppingCart.objects.all()
	serializer_class = ShoppingCartSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

	def get_queryset(self):
		"""
		只返回当前登录用户的购物车记录
		"""
		return ShoppingCart.objects.filter(user=self.request.user)

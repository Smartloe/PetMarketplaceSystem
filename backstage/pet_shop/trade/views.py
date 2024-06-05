from rest_framework import viewsets
from .models import OrderInfos, OrderGoods, ShoppingCart
from .serializers import OrderInfosSerializer, OrderGoodsSerializer, ShoppingCartSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class OrderInfosViewSet(viewsets.ModelViewSet):
	queryset = OrderInfos.objects.all()
	serializer_class = OrderInfosSerializer

	def get_queryset(self):
		"""
		只返回当前登录用户的订单记录
		"""
		return OrderInfos.objects.filter(user=self.request.user)


class OrderGoodsViewSet(viewsets.ModelViewSet):
	queryset = OrderGoods.objects.all()
	serializer_class = OrderGoodsSerializer

	def get_queryset(self):
		"""
		只返回当前登录用户的订单商品记录
		"""
		return OrderGoods.objects.filter(order__user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
# @csrf_exempt
class ShoppingCartViewSet(viewsets.ModelViewSet):
	queryset = ShoppingCart.objects.all()
	serializer_class = ShoppingCartSerializer

	def get_queryset(self):
		"""
		只返回当前登录用户的购物车记录
		"""
		return ShoppingCart.objects.filter(user=self.request.user)

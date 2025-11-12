from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import OrderInfos, OrderGoods, ShoppingCart
from .serializers import OrderInfosSerializer, OrderGoodsSerializer, ShoppingCartSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class OrderInfosViewSet(viewsets.ModelViewSet):
	queryset = OrderInfos.objects.all()
	serializer_class = OrderInfosSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		只返回当前登录用户的订单记录
		"""
		return OrderInfos.objects.filter(user=self.request.user)


class OrderGoodsViewSet(viewsets.ModelViewSet):
	queryset = OrderGoods.objects.all()
	serializer_class = OrderGoodsSerializer
	permission_classes = [permissions.IsAuthenticated]

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
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		只返回当前登录用户的购物车记录
		"""
		return ShoppingCart.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def create(self, request, *args, **kwargs):
		user = request.user
		commodity_id = request.data.get('commodity')
		quantity = int(request.data.get('quantity', 1))

		if not commodity_id:
			return Response({'detail': '请选择商品'}, status=status.HTTP_400_BAD_REQUEST)

		cart, created = ShoppingCart.objects.get_or_create(
			user=user,
			commodity_id=commodity_id,
			defaults={'quantity': quantity}
		)
		if not created:
			cart.quantity += quantity
			cart.save(update_fields=['quantity'])

		serializer = self.get_serializer(cart)
		return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

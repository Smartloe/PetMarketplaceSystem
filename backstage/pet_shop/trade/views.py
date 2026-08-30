from rest_framework import mixins, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import OrderInfos, OrderGoods, ShoppingCart
from .serializers import OrderInfosSerializer, OrderGoodsSerializer, ShoppingCartSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class OrderInfosViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
						mixins.DestroyModelMixin, viewsets.GenericViewSet):
	"""
	订单列表/详情/取消。金额与状态一律走专用端点
	（checkout / pay / refund / confirm）流转：此前这里挂的是完整
	ModelViewSet，登录用户可以直接 PUT 改单金额、伪造签收状态。
	"""
	queryset = OrderInfos.objects.all()
	serializer_class = OrderInfosSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		只返回当前登录用户的订单记录
		使用select_related优化查询，避免N+1问题
		"""
		return OrderInfos.objects.filter(user=self.request.user).select_related(
			'address', 'user'
		)

	def perform_destroy(self, instance):
		# “取消订单”只允许撤掉尚未支付的订单；已付款订单走 refund 端点。
		if instance.order_status != 0:
			raise ValidationError({'detail': '仅待支付订单可以取消'})
		instance.delete()


class OrderGoodsViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	订单商品只读。行的创建/数量修改只随结算流程发生，
	此前可写时客户端能把商品行搬进任意订单号下。
	"""
	queryset = OrderGoods.objects.all()
	serializer_class = OrderGoodsSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		只返回当前登录用户的订单商品记录
		使用select_related优化查询，避免N+1问题
		"""
		return OrderGoods.objects.filter(order__user=self.request.user).select_related(
			'order', 'goods', 'goods__types'
		)


@method_decorator(csrf_exempt, name='dispatch')
# @csrf_exempt
class ShoppingCartViewSet(viewsets.ModelViewSet):
	queryset = ShoppingCart.objects.all()
	serializer_class = ShoppingCartSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		"""
		只返回当前登录用户的购物车记录
		使用select_related优化查询，避免N+1问题
		"""
		return ShoppingCart.objects.filter(user=self.request.user).select_related(
			'commodity', 'commodity__types'
		)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def create(self, request, *args, **kwargs):
		user = request.user
		commodity_id = request.data.get('commodity')
		# 裸 int() 遇到非数字会抛 ValueError 变成 500；0 和负数会造出
		# 违背直觉的购物车行。
		try:
			quantity = int(request.data.get('quantity', 1))
		except (TypeError, ValueError):
			return Response({'detail': '购买数量无效'}, status=status.HTTP_400_BAD_REQUEST)
		if quantity < 1:
			return Response({'detail': '购买数量至少为 1'}, status=status.HTTP_400_BAD_REQUEST)

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

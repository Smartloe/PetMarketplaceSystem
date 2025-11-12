from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from customer_operation.models import UserAddress, UserComment
from .models import ShoppingCart, OrderInfos, OrderGoods


class CheckoutView(APIView):
	"""
	Mock checkout endpoint:
	- Validates selected cart items and shipping address
	- Creates an order + order goods items
	- Removes the processed cart entries
	"""
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		cart_ids = request.data.get('cart_ids') or []
		address_id = request.data.get('address_id')
		pay_method = int(request.data.get('pay_method', 1))
		leave_comment = request.data.get('leave_comment', '')

		if not cart_ids or not isinstance(cart_ids, list):
			return Response({'detail': '请选择要结算的商品'}, status=status.HTTP_400_BAD_REQUEST)

		if not address_id:
			return Response({'detail': '请先创建收货地址'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			address = UserAddress.objects.get(id=address_id, user=request.user)
		except UserAddress.DoesNotExist:
			return Response({'detail': '收货地址不存在或无权限访问'}, status=status.HTTP_400_BAD_REQUEST)

		carts = list(
			ShoppingCart.objects.filter(id__in=cart_ids, user=request.user).select_related('commodity')
		)
		if not carts:
			return Response({'detail': '购物车商品不存在'}, status=status.HTTP_400_BAD_REQUEST)

		total_price = Decimal('0.00')
		for cart in carts:
			if not cart.commodity:
				return Response({'detail': '有商品已下架，无法结算'}, status=status.HTTP_400_BAD_REQUEST)
			total_price += Decimal(str(cart.commodity.price)) * cart.quantity

		order_sn = timezone.now().strftime('%Y%m%d%H%M%S') + f'{request.user.id:04d}'
		order = OrderInfos.objects.create(
			user=request.user,
			order_sn=order_sn,
			address=address,
			total_price=total_price,
			coupon_price=Decimal('0.00'),
			payable_price=total_price,
			pay_method=pay_method,
			leave_comment=leave_comment,
			order_status=2,
			created_by=request.user.username,
			update_by=request.user.username
		)

		order_goods_payload = []
		for cart in carts:
			order_goods_payload.append(OrderGoods(
				order=order,
				goods=cart.commodity,
				goods_num=cart.quantity
			))
		OrderGoods.objects.bulk_create(order_goods_payload)
		ShoppingCart.objects.filter(id__in=[cart.id for cart in carts]).delete()

		return Response(
			{
				'order_id': order.id,
				'order_sn': order.order_sn,
				'payable_price': str(order.payable_price),
				'pay_method': order.pay_method
			},
			status=status.HTTP_201_CREATED
		)


class OrderRefundView(APIView):
	"""
	User applies for refund: mark refund_status pending and store reason for admin review.
	"""
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		reason = (request.data.get('reason') or '').strip()
		refund_type = request.data.get('refund_type') or ''

		if not reason:
			return Response({'detail': '请填写退款原因'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			order = OrderInfos.objects.get(id=order_id, user=request.user)
		except OrderInfos.DoesNotExist:
			return Response({'detail': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

		if order.order_status < 3:
			return Response({'detail': '请确认收货后再申请退款'}, status=status.HTTP_400_BAD_REQUEST)

		if order.confirmed_time:
			if timezone.now() - order.confirmed_time > timedelta(days=7):
				return Response({'detail': '确认收货超过7天，暂不支持退款'}, status=status.HTTP_400_BAD_REQUEST)

		if order.refund_status == 1:
			return Response({'detail': '退款申请正在审核中，请勿重复提交'}, status=status.HTTP_400_BAD_REQUEST)

		order.refund_status = 1
		order.order_status = 4  # 退货中
		order.refund_reason = f'{refund_type} - {reason}' if refund_type else reason
		order.save(update_fields=['refund_status', 'order_status', 'refund_reason', 'update_by', 'update_time'])

		return Response({'detail': '退款申请已提交，等待管理员审核'}, status=status.HTTP_200_OK)


class ConfirmReceiptView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		try:
			order = OrderInfos.objects.get(id=order_id, user=request.user)
		except OrderInfos.DoesNotExist:
			return Response({'detail': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

		if order.order_status < 2:
			return Response({'detail': '订单尚未发货'}, status=status.HTTP_400_BAD_REQUEST)
		if order.order_status >= 3:
			return Response({'detail': '订单已确认收货'}, status=status.HTTP_400_BAD_REQUEST)

		order.order_status = 3
		order.confirmed_time = timezone.now()
		order.save(update_fields=['order_status', 'confirmed_time', 'update_by', 'update_time'])
		return Response({'detail': '确认收货成功'}, status=status.HTTP_200_OK)


class OrderGoodsCommentView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id, order_goods_id):
		content = (request.data.get('content') or '').strip()
		rating = int(request.data.get('rating', 5))
		if not content:
			return Response({'detail': '请填写评价内容'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			order = OrderInfos.objects.get(id=order_id, user=request.user)
		except OrderInfos.DoesNotExist:
			return Response({'detail': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

		if order.order_status < 3:
			return Response({'detail': '订单未确认收货，暂不能评价'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			order_goods = OrderGoods.objects.get(id=order_goods_id, order=order)
		except OrderGoods.DoesNotExist:
			return Response({'detail': '订单商品不存在'}, status=status.HTTP_404_NOT_FOUND)

		if order_goods.commented:
			return Response({'detail': '该商品已评价'}, status=status.HTTP_400_BAD_REQUEST)

		UserComment.objects.create(
			user=request.user,
			commodity=order_goods.goods,
			content=content,
			rating=rating
		)
		order_goods.commented = True
		order_goods.save(update_fields=['commented'])

		return Response({'detail': '评价成功'}, status=status.HTTP_201_CREATED)

from decimal import Decimal
from datetime import timedelta
from uuid import uuid4

from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from commodity.models import CommodityInfos
from customer_operation.models import UserAddress, UserComment
from .models import ShoppingCart, OrderInfos, OrderGoods

# 评分允许的区间，与 UserComment.rating 的 help_text 一致
RATING_MIN = 1
RATING_MAX = 5

# 与 OrderInfos.pay_method 的 choices 保持一致：1 微信 / 2 支付宝 / 3 银联
VALID_PAY_METHODS = {1, 2, 3}


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
		leave_comment = request.data.get('leave_comment', '')

		# 裸 int() 遇到非数字会抛 ValueError 变成 500；且必须限定在
		# OrderInfos.pay_method 的 choices 内。
		try:
			pay_method = int(request.data.get('pay_method', 1))
		except (TypeError, ValueError):
			return Response({'detail': '支付方式无效'}, status=status.HTTP_400_BAD_REQUEST)
		if pay_method not in VALID_PAY_METHODS:
			return Response({'detail': '支付方式无效'}, status=status.HTTP_400_BAD_REQUEST)

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

		if any(cart.commodity is None for cart in carts):
			return Response({'detail': '有商品已下架，无法结算'}, status=status.HTTP_400_BAD_REQUEST)

		# 同一商品可能出现在多个购物车行里，先按商品汇总需要的数量
		wanted_by_commodity_id: dict[int, int] = {}
		for cart in carts:
			wanted_by_commodity_id[cart.commodity_id] = (
				wanted_by_commodity_id.get(cart.commodity_id, 0) + cart.quantity
			)

		# 整个结算过程放进一个事务：建单、写订单商品、扣库存、清购物车
		# 必须全部成功或全部回滚，否则会留下孤儿订单或已清空却没下单的购物车。
		try:
			with transaction.atomic():
				# 按 id 升序锁定商品行，顺序一致可避免并发结算相互死锁。
				# 加锁后再校验库存，防止两个请求同时通过校验导致超卖。
				locked = {
					item.id: item
					for item in CommodityInfos.objects.select_for_update()
					.filter(id__in=sorted(wanted_by_commodity_id))
					.order_by('id')
				}

				if len(locked) != len(wanted_by_commodity_id):
					return Response(
						{'detail': '有商品已下架，无法结算'},
						status=status.HTTP_400_BAD_REQUEST,
					)

				insufficient = [
					locked[cid].sku_title
					for cid, wanted in wanted_by_commodity_id.items()
					if (locked[cid].stock_quantity or 0) < wanted
				]
				if insufficient:
					return Response(
						{'detail': f'库存不足：{"、".join(insufficient)}'},
						status=status.HTTP_400_BAD_REQUEST,
					)

				total_price = sum(
					(Decimal(str(locked[cart.commodity_id].price)) * cart.quantity for cart in carts),
					Decimal('0.00'),
				)

				# 秒级时间戳 + 用户 id 不足以保证唯一（同一用户同一秒下两单
				# 就会撞 unique 约束并抛 500），补一段随机后缀。
				order_sn = (
					timezone.now().strftime('%Y%m%d%H%M%S')
					+ f'{request.user.id:04d}'
					+ uuid4().hex[:6]
				)
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

				OrderGoods.objects.bulk_create([
					OrderGoods(order=order, goods_id=cart.commodity_id, goods_num=cart.quantity)
					for cart in carts
				])

				# 真正扣减库存并累加销量。此前这两个字段从不更新，
				# 导致可以无限超卖，后台的“低库存提醒”也永远不变。
				for commodity_id, wanted in wanted_by_commodity_id.items():
					CommodityInfos.objects.filter(id=commodity_id).update(
						stock_quantity=F('stock_quantity') - wanted,
						sold=F('sold') + wanted,
					)

				ShoppingCart.objects.filter(id__in=[cart.id for cart in carts]).delete()
		except IntegrityError:
			return Response(
				{'detail': '下单失败，请重试'},
				status=status.HTTP_409_CONFLICT,
			)

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

		if order.order_status < 2:
			return Response({'detail': '订单尚未发货，无法申请退款'}, status=status.HTTP_400_BAD_REQUEST)
		
		if order.order_status == 5:
			return Response({'detail': '订单已退货，无法重复申请'}, status=status.HTTP_400_BAD_REQUEST)

		# 只有已签收的订单才检查7天退货期限
		if order.order_status == 3 and order.confirmed_time:
			if timezone.now() - order.confirmed_time > timedelta(days=7):
				return Response({'detail': '确认收货超过7天，暂不支持退款'}, status=status.HTTP_400_BAD_REQUEST)

		if order.refund_status == 1:
			return Response({'detail': '退款申请正在审核中，请勿重复提交'}, status=status.HTTP_400_BAD_REQUEST)

		# 条件更新防并发：两个请求同时通过上面的检查时，只有第一个
		# 能把 refund_status 置 1，第二个 update 命中 0 行。
		updated = OrderInfos.objects.filter(
			id=order.id, order_status__gte=2,
		).exclude(order_status=5).exclude(refund_status=1).update(
			refund_status=1,
			order_status=4,  # 退货中
			refund_reason=f'{refund_type} - {reason}' if refund_type else reason,
			update_by=request.user.username,
			update_time=timezone.now(),
		)
		if not updated:
			return Response({'detail': '退款申请正在审核中，请勿重复提交'}, status=status.HTTP_400_BAD_REQUEST)

		return Response({'detail': '退款申请已提交，等待管理员审核'}, status=status.HTTP_200_OK)


class OrderPayView(APIView):
	"""
	模拟支付：把未支付订单标记为已支付并记录支付方式。
	此前客户端直接 PUT /trade/orders/ 改 order_status（那个通道已因
	越权篡改风险关闭），支付必须走这个专用端点并校验前置状态。
	"""
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		try:
			pay_method = int(request.data.get('pay_method', 1))
		except (TypeError, ValueError):
			return Response({'detail': '支付方式无效'}, status=status.HTTP_400_BAD_REQUEST)
		if pay_method not in VALID_PAY_METHODS:
			return Response({'detail': '支付方式无效'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			order = OrderInfos.objects.get(id=order_id, user=request.user)
		except OrderInfos.DoesNotExist:
			return Response({'detail': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

		# 条件更新防并发：并发支付同一订单只有第一个生效
		updated = OrderInfos.objects.filter(
			id=order.id, user=request.user, order_status=0,
		).update(
			order_status=1,
			pay_method=pay_method,
			update_by=request.user.username,
			update_time=timezone.now(),
		)
		if not updated:
			return Response({'detail': '订单不是待支付状态'}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'detail': '支付成功'}, status=status.HTTP_200_OK)


class CancelOrderRefundView(APIView):
	"""
	撤销退款申请：只有“待审核”的申请可以由用户自行撤回，
	订单随之回到发货中状态（与 OrderRefundView 申请时置的状态对应）。
	"""
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		try:
			order = OrderInfos.objects.get(id=order_id, user=request.user)
		except OrderInfos.DoesNotExist:
			return Response({'detail': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

		# 条件更新防并发：并发撤销只有第一个生效
		updated = OrderInfos.objects.filter(
			id=order.id, user=request.user, refund_status=1,
		).update(
			refund_status=0,
			order_status=2,
			update_by=request.user.username,
			update_time=timezone.now(),
		)
		if not updated:
			return Response({'detail': '没有待审核的退款申请'}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'detail': '已撤销退款申请'}, status=status.HTTP_200_OK)


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

		# 条件更新防并发：重复的确认收货请求只有第一个生效
		updated = OrderInfos.objects.filter(
			id=order.id, order_status__gte=2, order_status__lt=3,
		).update(
			order_status=3,
			confirmed_time=timezone.now(),
			update_by=request.user.username,
			update_time=timezone.now(),
		)
		if not updated:
			return Response({'detail': '订单已确认收货'}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'detail': '确认收货成功'}, status=status.HTTP_200_OK)


class OrderGoodsCommentView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id, order_goods_id):
		content = (request.data.get('content') or '').strip()
		if not content:
			return Response({'detail': '请填写评价内容'}, status=status.HTTP_400_BAD_REQUEST)

		# rating 之前既不挡非数字（500）也不挡越界值：传 999 会入库
		# 并污染后台平均分（超出 1-5 的值不计入星级分布却计入均值）。
		try:
			rating = int(request.data.get('rating', 5))
		except (TypeError, ValueError):
			return Response({'detail': '评分必须是 1 到 5 的整数'}, status=status.HTTP_400_BAD_REQUEST)
		if not RATING_MIN <= rating <= RATING_MAX:
			return Response({'detail': '评分必须是 1 到 5 的整数'}, status=status.HTTP_400_BAD_REQUEST)

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

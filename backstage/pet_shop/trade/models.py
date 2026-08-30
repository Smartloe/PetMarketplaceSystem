from django.db import models


# Create your models here.

# 订单信息表
class OrderInfos(models.Model):
	user = models.ForeignKey('auth.User', related_name='order', on_delete=models.CASCADE, verbose_name='用户')
	order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
	address = models.ForeignKey(
		'customer_operation.UserAddress', to_field="id",
		on_delete=models.CASCADE, verbose_name='地址'
	)
	total_price = models.DecimalField(max_digits=24, decimal_places=2, verbose_name='总金额')
	coupon_price = models.DecimalField(
		max_digits=24, decimal_places=2,
		verbose_name='优惠金额',
		null=True, blank=True,
		default=0.00
	)
	payable_price = models.DecimalField(max_digits=24, decimal_places=2, verbose_name='应付金额')
	pay_method = models.SmallIntegerField(
		choices=((1, "微信"), (2, "支付宝"), (3, "银联")),
		verbose_name='支付方式',
		blank=True)
	leave_comment = models.CharField(max_length=1000, verbose_name='订单留言备注', blank=True)
	order_status = models.SmallIntegerField(
		choices=((0, "未支付"), (1, "已支付"), (2, '发货中'), (3, '已签收'), (4, '退货中'), (5, '已退货')),
		verbose_name='订单状态'
	)
	confirmed_time = models.DateTimeField(null=True, blank=True, verbose_name='确认收货时间')
	refund_status = models.SmallIntegerField(
		default=0,
		choices=((0, '无'), (1, '待审核'), (2, '已通过'), (3, '已拒绝')),
		verbose_name='退款状态'
	)
	refund_reason = models.CharField(max_length=255, blank=True, verbose_name='退款原因')
	created_by = models.CharField(max_length=255, verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	update_by = models.CharField(max_length=255, verbose_name='更新人', blank=True)
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '订单信息'
		verbose_name_plural = '订单信息'
		# 分页必须建立在有序 queryset 上，否则跨页会重复或漏行
		ordering = ['-created_time', '-id']
		indexes = [
			models.Index(fields=['user'], name='idx_order_user'),
			models.Index(fields=['order_sn'], name='idx_order_sn'),
			models.Index(fields=['order_status'], name='idx_order_status'),
			models.Index(fields=['created_time'], name='idx_order_created'),
			models.Index(fields=['refund_status'], name='idx_order_refund'),
			# 复合索引：用于用户订单列表查询（用户+状态+创建时间）
			models.Index(fields=['user', 'order_status', 'created_time'], name='idx_order_user_list'),
		]

	def __str__(self):
		return f"订单号: {self.order_sn}, 用户: {self.user.username}"


class OrderGoods(models.Model):
	"""
	订单的商品详情
	"""
	order = models.ForeignKey(OrderInfos, on_delete=models.CASCADE, verbose_name="订单信息", related_name="goods")
	# PROTECT：删除商品不允许连带销毁历史订单明细，否则订单金额与
	# 明细对不上，审计数据失真。要下架请改 status 而不是删行。
	goods = models.ForeignKey('commodity.CommodityInfos', on_delete=models.PROTECT, verbose_name="商品")
	goods_num = models.IntegerField(default=1, verbose_name="商品数量")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	commented = models.BooleanField(default=False, verbose_name='已评论')

	class Meta:
		verbose_name = "订单商品"
		verbose_name_plural = verbose_name
		ordering = ['-add_time', '-id']

	def __str__(self):
		return f"订单号: {self.order.order_sn}, 商品: {self.goods.sku_title}"


# 购物车信息表
class ShoppingCart(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='用户')
	# db_constraint 已恢复（此前为 False）：无 FK 约束时客户端可以塞进
	# 任意 commodity_id 造出脏行。加购接口同时校验商品存在。
	commodity = models.ForeignKey(
		'commodity.CommodityInfos',
		on_delete=models.SET_NULL,
		null=True,
		blank=True, verbose_name='商品'
	)
	quantity = models.IntegerField('购买数量')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = '购物车'
		verbose_name_plural = '购物车'
		ordering = ['-created_time', '-id']
		indexes = [
			models.Index(fields=['user'], name='idx_cart_user'),
			models.Index(fields=['commodity'], name='idx_cart_commodity'),
			# 复合索引：用于用户购物车查询（用户+商品）
			models.Index(fields=['user', 'commodity'], name='idx_cart_user_commodity'),
		]

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
	created_by = models.CharField(max_length=255, verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	update_by = models.CharField(max_length=255, verbose_name='更新人', blank=True)
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '订单信息'
		verbose_name_plural = '订单信息'


class OrderGoods(models.Model):
	"""
	订单的商品详情
	"""
	order = models.ForeignKey(OrderInfos, on_delete=models.CASCADE, verbose_name="订单信息", related_name="goods")
	goods = models.ForeignKey('commodity.CommodityInfos', on_delete=models.CASCADE, verbose_name="商品")
	goods_num = models.IntegerField(default=0, verbose_name="商品数量")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

	class Meta:
		verbose_name = "订单商品"
		verbose_name_plural = verbose_name

	def __str__(self):
		return str(self.order.order_sn)


# 购物车信息表
class ShoppingCart(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='用户')
	commodity = models.ForeignKey(
		'commodity.CommodityInfos',
		on_delete=models.SET_NULL,
		db_constraint=False, null=True,
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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# 用户信息表
class UserInfos(models.Model):
	nick_name = models.CharField(max_length=90, verbose_name='用户昵称', help_text='用户昵称')
	user_intro = models.CharField(max_length=900, verbose_name='个性签名', blank=True, help_text='个性签名')
	avatar = models.ImageField(verbose_name='头像图片', upload_to="profile_photo/", blank=True, help_text='头像图片')
	email = models.EmailField(verbose_name='邮件地址', help_text='邮件地址', unique=True)
	phone = PhoneNumberField(verbose_name='手机号', blank=True, help_text='手机号')
	user_status = models.SmallIntegerField(default=1, verbose_name='用户状态', choices=((0, "冻结"), (1, "正常")))
	token = models.CharField(max_length=255, verbose_name='令牌', blank=True)
	user_score = models.PositiveIntegerField(verbose_name='用户打分', null=True, blank=True, default=80)
	total_cost_amt = models.DecimalField(
		max_digits=24, decimal_places=6,
		verbose_name='累计消费金额', null=True,
		blank=True, default=0.00
	)
	last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return self.nick_name

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'


# 订单信息表
class OrderInfos(models.Model):
	user = models.ForeignKey('UserInfos', related_name='orders', on_delete=models.CASCADE, verbose_name='用户')
	address = models.ForeignKey('Address', to_field="id", on_delete=models.CASCADE, verbose_name='地址')
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


# 购物车信息表
class Cart(models.Model):
	quantity = models.IntegerField('购买数量')
	commodityInfos = models.ForeignKey(
		'commodity.CommodityInfos',
		on_delete=models.SET_NULL,
		db_constraint=False, null=True,
		blank=True, verbose_name='商品信息'
	)
	user = models.ForeignKey(UserInfos, on_delete=models.CASCADE, verbose_name='用户')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = '购物车'
		verbose_name_plural = '购物车'

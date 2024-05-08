from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


# 用户信息表
class UserInfos(AbstractBaseUser):
	nick_name = models.CharField(max_length=90, verbose_name='用户昵称', help_text='用户昵称')
	user_intro = models.CharField(max_length=900, verbose_name='个性签名', blank=True, help_text='个性签名')
	avatar = models.ImageField(verbose_name='头像图片', upload_to="profile_photos/", blank=True, help_text='头像图片')
	email = models.EmailField(verbose_name='邮件地址', help_text='邮件地址')
	phone = PhoneNumberField(verbose_name='手机号', blank=True, help_text='手机号')
	user_status = models.SmallIntegerField(default=1, verbose_name='用户状态', choices=((0, "冻结"), (1, "正常")))
	token = models.CharField(max_length=255, verbose_name='令牌', blank=True)
	user_score = models.PositiveIntegerField(verbose_name='用户打分', null=True, blank=True, default=80)
	total_cost_amt = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='累计消费金额', null=True,
	                                     blank=True, default=0.00)
	last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'


# 订单信息表
class OrderInfos(models.Model):
	user = models.ForeignKey(UserInfos, related_name='orders', on_delete=models.CASCADE, verbose_name='用户')
	address = models.ForeignKey('Address', on_delete=models.CASCADE, verbose_name='地址')
	total_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='总金额')
	coupon_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='优惠金额', null=True, blank=True,
	                                   default=0.00)
	payable_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='应付金额')
	pay_method = models.SmallIntegerField(choices=((1, "微信"), (2, "支付宝"), (3, "银联")), verbose_name='支付方式',
	                                      blank=True)
	leave_comment = models.CharField(max_length=1000, verbose_name='订单留言备注', blank=True)
	order_status = models.SmallIntegerField(
		choices=((0, "未支付"), (1, "已支付"), (2, '发货中'), (3, '已签收'), (4, '退货中')), verbose_name='订单状态')
	created_by = models.ForeignKey(UserInfos, related_name='created_orders', on_delete=models.SET_NULL, null=True,
	                               verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

	class Meta:
		verbose_name = '订单信息'
		verbose_name_plural = '订单信息'


# 购物车信息表
class Cart(models.Model):
	quantity = models.IntegerField('购买数量')
	commodityInfos = models.ForeignKey('CommodityInfos', on_delete=models.SET_NULL, db_constraint=False, null=True,
	                                   blank=True, verbose_name='商品信息')
	user = models.ForeignKey(UserInfos, on_delete=models.CASCADE, verbose_name='用户')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = '购物车'
		verbose_name_plural = '购物车'


# 收货地址信息表
class Address(models.Model):
	user = models.ForeignKey(UserInfos, related_name='addresses', on_delete=models.CASCADE, verbose_name='用户')
	address_name = models.CharField(max_length=255, verbose_name='地址名称')
	seq_number = models.PositiveIntegerField(verbose_name='顺序号')
	province = models.CharField(max_length=255, verbose_name='省')
	city = models.CharField(max_length=255, verbose_name='市')
	county = models.CharField(max_length=255, verbose_name='区')
	street = models.CharField(max_length=255, verbose_name='街道')
	last_detail = models.CharField(max_length=255, verbose_name='门牌号')
	is_default = models.BooleanField(default=False, verbose_name='是否为默认地址')
	created_by = models.ForeignKey(UserInfos, related_name='created_addresses', on_delete=models.SET_NULL, null=True,
	                               verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.ForeignKey(UserInfos, related_name='updated_addresses', on_delete=models.SET_NULL, null=True,
	                               verbose_name='更新人', blank=True)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '收货地址信息'
		verbose_name_plural = '收货地址信息'


# 广告信息表
class Advertisement(models.Model):
	ad_title = models.CharField(max_length=255, verbose_name='广告标题')
	ad_content = models.CharField(max_length=255, verbose_name='广告内容')
	ad_image = models.ImageField(verbose_name='广告图片', upload_to="ad_photos/")
	ad_link = models.CharField(max_length=255, verbose_name='广告链接')
	start_date = models.DateTimeField(verbose_name='广告开始时间', null=True, blank=True)
	end_date = models.DateTimeField(verbose_name='广告结束时间', null=True, blank=True)
	click_count = models.IntegerField(verbose_name='点击次数', default=0)
	created_by = models.ForeignKey(UserInfos, related_name='created_ads', on_delete=models.SET_NULL, null=True,
	                               verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.ForeignKey(UserInfos, related_name='updated_ads', on_delete=models.SET_NULL, null=True,
	                               verbose_name='更新人', blank=True)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '广告信息'
		verbose_name_plural = '广告信息'


# 商品信息表
class CommodityInfos(models.Model):
	sku_title = models.CharField(max_length=255, verbose_name='商品名称')
	sku_description = models.CharField(max_length=255, verbose_name='商品描述', blank=True)
	main_image = models.ImageField(verbose_name='商品主图', upload_to="product_photos/")
	detail_images = models.CharField(max_length=255, verbose_name='商品细节图', blank=True)
	cost_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='商品进价', blank=True)
	price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='商品售价')
	status = models.CharField(max_length=32, default='1', verbose_name='商品状态')
	stock_quantity = models.PositiveIntegerField(verbose_name='库存数量', blank=True)
	created_by = models.ForeignKey(UserInfos, related_name='created_commodities', on_delete=models.SET_NULL, null=True,
	                               verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.ForeignKey(UserInfos, related_name='updated_commodities', on_delete=models.SET_NULL, null=True,
	                               verbose_name='更新人', blank=True)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '商品信息'
		verbose_name_plural = '商品信息'


# 商品类型表
class ProductCategories(models.Model):
	title = models.CharField('一级类型', max_length=100)
	parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
	                                    related_name='sub_categories', verbose_name='父级类型')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = '商品类型'
		verbose_name_plural = '商品类型'


# 管理员信息表
class Admin(AbstractBaseUser):
	username = models.CharField(max_length=255, verbose_name='姓名', unique=True)
	phone_number = PhoneNumberField(verbose_name="电话")
	is_active = models.SmallIntegerField(choices=((0, "未激活"), (1, "已激活")), verbose_name='管理员状态', default=1)
	created_by = models.ForeignKey('self', related_name='created_admins', on_delete=models.SET_NULL, null=True,
	                               verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)

	class Meta:
		verbose_name = '管理员信息'
		verbose_name_plural = '管理员信息'

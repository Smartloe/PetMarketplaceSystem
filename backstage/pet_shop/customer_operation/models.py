from django.db import models


# Create your models here.
class UserFav(models.Model):
	"""
	用户收藏
	"""
	user = models.ForeignKey('customer.UserInfos', verbose_name="用户")
	goods = models.ForeignKey('commodity.CommodityInfos', verbose_name="商品", help_text="商品id")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

	class Meta:
		verbose_name = '用户收藏'
		verbose_name_plural = verbose_name
		unique_together = ("user", "goods")

	def __str__(self):
		return self.user.nick_name


class UserLeavingMessage(models.Model):
	"""
	用户留言
	"""
	MESSAGE_CHOICES = (
		(1, "留言"),
		(2, "投诉"),
		(3, "询问"),
		(4, "售后"),
		(5, "求购")
	)
	user = models.ForeignKey('customer.UserInfos', verbose_name="用户")
	message_type = models.IntegerField(
		default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
		help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)"
	)
	subject = models.CharField(max_length=100, default="", verbose_name="主题")
	message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
	file = models.FileField(upload_to="media/leaving_message_imgs/", verbose_name="上传的文件", help_text="上传的文件")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

	class Meta:
		verbose_name = "用户留言"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.subject


class UserAddress(models.Model):
	"""
	用户收货地址
	"""
	user = models.ForeignKey('customer.UserInfos', verbose_name="用户")
	province = models.CharField(max_length=100, default="", verbose_name="省")
	city = models.CharField(max_length=100, default="", verbose_name="市")
	county = models.CharField(max_length=100, default="", verbose_name="区/县")
	address = models.CharField(max_length=100, default="", verbose_name="详细地址")
	is_default = models.BooleanField(default=False, verbose_name='是否为默认地址')
	signer_name = models.CharField(max_length=100, default="", verbose_name="收件人")
	signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
	created_by = models.CharField(null=True, max_length=255, verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.CharField(null=True, max_length=255, verbose_name='更新人', blank=True)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = "收货地址"
		verbose_name_plural = verbose_name

	def __str__(self):
		return f"{self.province}{self.city}{self.county}{self.address}"

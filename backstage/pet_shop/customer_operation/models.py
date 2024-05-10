from django.db import models


# Create your models here.
class UserFav(models.Model):
	"""
	用户收藏
	"""
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="用户")
	goods = models.ForeignKey(
		'commodity.CommodityInfos', on_delete=models.CASCADE,
		verbose_name="商品", help_text="商品id"
	)
	add_time = models.DateTimeField(auto_now_add=True, verbose_name=u"添加时间")

	class Meta:
		verbose_name = '用户收藏'
		verbose_name_plural = verbose_name
		unique_together = ("user", "goods")

	def __str__(self):
		return self.user.username


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
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="用户")
	message_type = models.IntegerField(
		default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
		help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)"
	)
	subject = models.CharField(max_length=100, default="", verbose_name="主题")
	message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
	file = models.FileField(
		upload_to="leaving_message_imgs/",
		verbose_name="上传的文件", help_text="上传的文件",
		null=True, blank=True
	)
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
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="用户")
	province = models.CharField(max_length=100, default="", verbose_name="省/直辖市")
	city = models.CharField(max_length=100, default="", verbose_name="市")
	county = models.CharField(max_length=100, default="", verbose_name="区/县")
	address = models.CharField(max_length=100, default="", verbose_name="详细地址")
	is_default = models.BooleanField(default=False, verbose_name='是否为默认地址')
	signer_name = models.CharField(max_length=100, default="", verbose_name="收件人")
	signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
	created_by = models.CharField(null=True, max_length=255, verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.CharField(null=True, max_length=255, verbose_name='更新人', blank=True)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = "收货地址"
		verbose_name_plural = verbose_name

	def __str__(self):
		return f"{self.province}{self.city}{self.county}{self.address}"


class UserComment(models.Model):
	"""
	用户商品评论
	"""
	# 关联到用户模型，假设使用Django内置的User模型
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="用户")
	# 关联到商品模型，假设您的商品模型位于commodity应用下，名为Commodity
	commodity = models.ForeignKey('commodity.CommodityInfos', on_delete=models.CASCADE, verbose_name="商品")
	# 评论内容
	content = models.TextField(verbose_name="评论内容")
	# 评论星级，范围1-5
	rating = models.IntegerField(default=5, verbose_name="评分", help_text="评分范围从1到5")
	# 是否显示，用于审核评论
	is_show = models.BooleanField(default=True, verbose_name="是否展示")
	# 创建人，可以为空或者匿名用户
	created_by = models.CharField(max_length=255, null=True, blank=True, verbose_name='创建人')
	# 创建时间，自动设置为当前时间
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

	class Meta:
		verbose_name = "用户评论"
		verbose_name_plural = verbose_name

	def __str__(self):
		# 返回评论的摘要或者其他有意义的字符串表示
		return f"评论用户：{self.user.username} - 商品：{self.commodity.sku_title} - 评分：{self.rating}"

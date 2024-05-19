from django.db import models


# Create your models here.
# 商品信息表
class CommodityInfos(models.Model):
	sku_title = models.CharField(max_length=255, verbose_name='商品名称')
	sku_description = models.CharField(max_length=255, verbose_name='商品描述', blank=True)
	main_image = models.ImageField(verbose_name='商品主图', upload_to="product_photos/")
	detail_images = models.ImageField(verbose_name='商品主图', upload_to="product_photos_details/")
	cost_price = models.DecimalField(max_digits=24, decimal_places=2, verbose_name='商品进价', blank=True)
	price = models.DecimalField(max_digits=24, decimal_places=2, verbose_name='商品售价')
	status = models.CharField(max_length=32, default='1', verbose_name='商品状态')
	types = models.ForeignKey(to='CommodityCategories', on_delete=models.CASCADE, verbose_name='商品类型')
	sold = models.IntegerField(verbose_name='已售数量', default=0)
	stock_quantity = models.PositiveIntegerField(verbose_name='库存数量', blank=True)
	created_by = models.CharField(null=True, verbose_name='创建人', blank=True, max_length=32)
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.CharField(null=True, verbose_name='更新人', blank=True, max_length=32)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '商品信息'
		verbose_name_plural = '商品信息'

	def __str__(self):
		return self.sku_title


# 商品类型表
class CommodityCategories(models.Model):
	title = models.CharField('类型', max_length=100, unique=True)
	parent_category = models.ForeignKey(
		'self', on_delete=models.CASCADE, null=True, blank=True,
		related_name='sub_categories', verbose_name='父级类型'
	)

	def __str__(self):
		# 如果有父级类型，返回 "父级类型 | 本类型"，否则只返回本类型
		if self.parent_category:
			return f"{self.parent_category.title} | {self.title}"
		else:
			return self.title

	class Meta:
		verbose_name = '商品类型'
		verbose_name_plural = '商品类型'

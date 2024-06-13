from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CommodityInfos, CommodityCategories


# 定义商品信息资源类，用于导入和导出
class CommodityInfosResource(resources.ModelResource):
	class Meta:
		model = CommodityInfos


# 定义商品类型资源类，用于导入和导出
class CommodityCategoriesResource(resources.ModelResource):
	class Meta:
		model = CommodityCategories


# 注册商品信息模型到admin，并增加导入导出功能
@admin.register(CommodityInfos)
class CommodityInfosAdmin(ImportExportModelAdmin):
	resource_class = CommodityInfosResource
	list_display = (
		'main_image_img', 'sku_title',
		'types', 'stock_quantity',
		'formatted_price',
	)
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 5
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['sku_title']

	# 格式化价格显示
	def formatted_price(self, obj):
		return "￥{0:.2f}".format(obj.price)

	formatted_price.admin_order_field = 'price'  # 允许按照价格字段排序
	formatted_price.short_description = '价格'

	# 显示商品主图
	def main_image_img(self, obj):
		if obj.main_image:
			return format_html('<img src="{}" width="80px" />', obj.main_image.url)
		return "-"

	main_image_img.short_description = '商品主图'


# 注册商品类型模型到admin，并增加导入导出功能
@admin.register(CommodityCategories)
class CommodityCategoriesAdmin(ImportExportModelAdmin):
	resource_class = CommodityCategoriesResource
	list_display = ('title', 'parent_category',)
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['title']

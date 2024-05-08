from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(CommodityInfos)
class CommodityInfosAdmin(admin.ModelAdmin):
	list_display = ('main_image_img', 'sku_title', 'types', 'stock_quantity', 'price',)  # 添加 main_image_img 到列表显示字段中
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 5
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['sku_title']

	def main_image_img(self, obj):
		if obj.main_image:
			return format_html('<img src="{}" width="80px" />', obj.main_image.url)
		return "-"

	main_image_img.short_description = '商品主图'


@admin.register(CommodityCategories)
class CommodityCategoriesAdmin(admin.ModelAdmin):
	list_display = ('title', 'parent_category',)
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['title']

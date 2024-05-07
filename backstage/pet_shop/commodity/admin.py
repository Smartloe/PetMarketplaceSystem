from django.contrib import admin
from django.utils.html import format_html
from .models import *


class CommodityInfosAdmin(admin.ModelAdmin):
	list_display = ('main_image_img', 'sku_title', 'types', 'price',)  # 添加 main_image_img 到列表显示字段中

	def main_image_img(self, obj):
		if obj.main_image:
			return format_html('<img src="{}" width="80px" />', obj.main_image.url)
		return "-"

	main_image_img.short_description = '商品主图'


admin.site.register(CommodityInfos, CommodityInfosAdmin)

admin.site.register(CommodityCategories)

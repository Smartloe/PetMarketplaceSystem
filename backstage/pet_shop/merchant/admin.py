from django.contrib import admin
from django.utils.html import format_html
from .models import *


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
	list_display = ['display_ad_image', 'ad_title', 'click_count', 'created_time']
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['ad_title']

	def display_ad_image(self, obj):
		return format_html('<img src="{}" height="30" />', obj.ad_image.url)

	display_ad_image.short_description = '广告图片'

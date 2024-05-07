from django.contrib import admin
from django.utils.html import format_html
from .models import *


# Register your models here.
class UserInfosAdmin(admin.ModelAdmin):
	list_display = ('get_user_avatar', "nick_name")  # 添加 avatar_and_nick_name 到列表显示字段中

	def get_user_avatar(self, obj):
		if obj.avatar and hasattr(obj.avatar, 'url'):  # 检查 avatar 字段是否有文件关联
			return format_html('<img src="{}" width="30px" />', obj.avatar.url)
		return "-"

	get_user_avatar.short_description = '头像'


admin.site.register(UserInfos, UserInfosAdmin)


class OrderInfosAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'user', 'address', 'total_price', 'payable_price',
		'order_status', 'created_by', 'created_time', 'update_by', 'update_time'
	)


admin.site.register(OrderInfos, OrderInfosAdmin)

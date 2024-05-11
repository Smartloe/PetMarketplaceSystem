from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(UserFav)
class UserFavAdmin(admin.ModelAdmin):
	list_display = ['user', 'goods', "add_time"]
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200


@admin.register(UserLeavingMessage)
class UserLeavingMessageAdmin(admin.ModelAdmin):
	list_display = ['user', 'message_type', "subject", "add_time"]
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
	list_display = ["signer_name", "signer_mobile", "is_default", "province", "city", "county", "address"]
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['signer_name', 'signer_mobile']


@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
	list_display = ["user", "commodity", "rating", "is_show", "created_time"]
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
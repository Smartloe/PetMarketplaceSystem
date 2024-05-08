from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
	list_display = ["user", "commodity", "quantity", ]
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['user', 'commodity']


@admin.register(OrderInfos)
class OrderInfosAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'user', 'address', 'total_price', 'payable_price',
		'order_status', 'created_by', 'created_time', 'update_by', 'update_time'
	)
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['user', 'created_by']

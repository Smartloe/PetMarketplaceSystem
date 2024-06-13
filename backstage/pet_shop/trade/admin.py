from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ShoppingCart, OrderInfos, OrderGoods


# Define resources for import/export
class ShoppingCartResource(resources.ModelResource):
	class Meta:
		model = ShoppingCart


class OrderInfosResource(resources.ModelResource):
	class Meta:
		model = OrderInfos


class OrderGoodsResource(resources.ModelResource):
	class Meta:
		model = OrderGoods


# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartAdmin(ImportExportModelAdmin):
	resource_class = ShoppingCartResource
	list_display = ["user", "commodity", "quantity"]
	list_per_page = 10
	list_max_show_all = 200
	search_fields = ['user', 'commodity']


@admin.register(OrderInfos)
class OrderInfosAdmin(ImportExportModelAdmin):
	resource_class = OrderInfosResource
	list_display = (
		'id', 'user', 'address', 'total_price', 'payable_price',
		'order_status', 'created_by', 'created_time', 'update_by', 'update_time'
	)
	list_per_page = 10
	list_max_show_all = 200
	search_fields = ['user__username', 'created_by']


@admin.register(OrderGoods)
class OrderGoodsAdmin(ImportExportModelAdmin):
	resource_class = OrderGoodsResource
	list_display = ('id', 'order', 'goods', 'goods_num', 'add_time')
	list_per_page = 10
	list_max_show_all = 200
	search_fields = ['order__order_sn', 'goods__name']

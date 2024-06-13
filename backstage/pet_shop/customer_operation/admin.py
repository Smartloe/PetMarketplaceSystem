from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import UserFav, UserLeavingMessage, UserAddress, UserComment


class UserFavResource(resources.ModelResource):
	class Meta:
		model = UserFav


class UserLeavingMessageResource(resources.ModelResource):
	class Meta:
		model = UserLeavingMessage


class UserAddressResource(resources.ModelResource):
	class Meta:
		model = UserAddress


class UserCommentResource(resources.ModelResource):
	class Meta:
		model = UserComment


@admin.register(UserFav)
class UserFavAdmin(ImportExportModelAdmin):
	resource_class = UserFavResource
	list_display = ['user', 'goods', "add_time"]
	list_per_page = 10
	list_max_show_all = 200


@admin.register(UserLeavingMessage)
class UserLeavingMessageAdmin(ImportExportModelAdmin):
	resource_class = UserLeavingMessageResource
	list_display = ['user', 'message_type', "subject", "is_replied", "add_time"]
	list_per_page = 10
	list_max_show_all = 200


@admin.register(UserAddress)
class UserAddressAdmin(ImportExportModelAdmin):
	resource_class = UserAddressResource
	list_display = ["signer_name", "signer_mobile", "is_default", "province", "city", "county", "address"]
	list_per_page = 10
	list_max_show_all = 200
	search_fields = ['signer_name', 'signer_mobile']


@admin.register(UserComment)
class UserCommentAdmin(ImportExportModelAdmin):
	resource_class = UserCommentResource
	list_display = ["user", "commodity", "rating", "is_show", "created_time"]
	list_per_page = 10
	list_max_show_all = 200

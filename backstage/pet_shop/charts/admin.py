from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from .models import SoldModel, UserModel


@admin.register(SoldModel)
class SoldModelAdmin(admin.ModelAdmin):
    change_list_template = "admin/charts/SoldModel/change_list.html"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


try:
    admin.site.unregister(UserModel)
except NotRegistered:
    pass

from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import UserProfile


# 定义用户信息资源类，用于导入和导出
class UserProfileResource(resources.ModelResource):
	class Meta:
		model = UserProfile


# 注册用户信息模型到admin，并增加导入导出功能
@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
	resource_class = UserProfileResource
	list_display = ('get_user_avatar', 'username', 'mobile')  # 添加 avatar_and_nick_name 到列表显示字段中
	# 在数据列表页设置每一页显示的数据量
	list_per_page = 10
	# 在数据列表页设置每一页显示最大上限的数据量
	list_max_show_all = 200
	# 设置可搜索的字段
	search_fields = ['username__username', 'mobile']

	# 显示用户头像
	def get_user_avatar(self, obj):
		if obj.avatar and hasattr(obj.avatar, 'url'):  # 检查 avatar 字段是否有文件关联
			return format_html('<img src="{}" width="30px" />', obj.avatar.url)
		return "-"

	get_user_avatar.short_description = '头像'

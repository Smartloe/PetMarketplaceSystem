"""
URL configuration for pet_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

# 设置管理后台的标题和头部
admin.site.site_header = '吉祥宠物商城管理'  # 设置管理后台的头部标题
admin.site.site_title = '吉祥宠物商城管理'  # 设置管理后台的标题
admin.site.index_title = '站点管理'  # 设置管理后台首页的标题

urlpatterns = [
	path('admin/', admin.site.urls),
	path('charts', include('charts.urls')),  # 数据可视化
	# 配置媒体资源的路由信息
	re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
	# 定义静态资源的路由信息
	re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]

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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# 设置管理后台的标题和头部
admin.site.site_header = '吉祥宠物商城管理后台'  # 设置管理后台的头部标题
admin.site.site_title = '吉祥宠物商城管理后台'  # 设置管理后台的标题
admin.site.index_title = '站点管理'  # 设置管理后台首页的标题

schema_view = get_schema_view(
	openapi.Info(
		title="宠物商城API",
		default_version='v1',
		description="吉祥宠物商城API接口文档",
		terms_of_service="https://www.yourcompany.com/terms/",
		contact=openapi.Contact(email="contact@yourapi.local"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=[permissions.AllowAny],
)
urlpatterns = [
	path('admin/', admin.site.urls),  # 后台管理
	path('accounts/', include('accounts.urls')),  # 账户模块
	path('operation/', include('customer_operation.urls')),  # 用户操作模块
	path('commodity/', include('commodity.urls')),  # 商品模块
	path('merchant/', include('merchant.urls')),  # 商家模块
	path('trade/', include('trade.urls')),  # 交易模块
	path('charts', include('charts.urls')),  # 数据可视化
	path('', include('index.urls')),  # 其他展示/工具模块
	# 配置媒体资源的路由信息
	re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
	# 定义静态资源的路由信息
	re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
	# drf-yasg
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

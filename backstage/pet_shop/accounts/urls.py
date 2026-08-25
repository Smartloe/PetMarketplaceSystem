# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/6 13:14
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/6 13:14
@Description:
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import *

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
urlpatterns = [
	path('', include(router.urls)),
	path('profiles/upload-avatar/', AvatarUploadView.as_view(), name='upload-avatar'),
	# 顾客注册
	path('register/', RegisterView.as_view(), name='register'),

	# 顾客登录（返回 access / refresh 一对 JWT）
	path('login/', LoginView.as_view(), name='login'),

	# 顾客登出
	path('loginout/', LogoutView.as_view(), name='logout'),

	# access token 过期后用 refresh token 换新的
	path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
	path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

	# 验证码
	path('captcha/', CaptchaView.as_view(), name='captcha'),

]

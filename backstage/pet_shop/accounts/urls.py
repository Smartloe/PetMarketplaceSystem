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
from .views import *

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
urlpatterns = [
	path('', include(router.urls)),
	# 顾客注册
	path('register/', RegisterView.as_view(), name='register'),

	# 顾客登录
	path('login/', LoginView.as_view(), name='login'),

	# 顾客登出
	path('loginout/', LogoutView.as_view(), name='login'),

	# 验证码
	path('captcha/', CaptchaView.as_view(), name='captcha'),

]

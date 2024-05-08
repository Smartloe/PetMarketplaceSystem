# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/6 13:14
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/6 13:14
@Description: 
"""
from django.urls import path
from .views import *

urlpatterns = [
	# Generic Class Based View
	path("register/", UserRegister.as_view(), name="user_register"),
	path("login/", UserLogin.as_view(), name="user_login"),
]

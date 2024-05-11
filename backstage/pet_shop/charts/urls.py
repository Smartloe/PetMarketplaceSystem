# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/11 10:20
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/11 10:20
@Description: 
"""
from django.urls import path
from .views import *

urlpatterns = [
	path('sold_data/', sold_data, name='sold_data'),
]

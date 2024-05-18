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
	path('list/', commodityView.as_view(), name='list'),
	path('detail/<int:pk>/', detailView.as_view(), name='detail'),
	path('search/', CommoditySearchView.as_view(), name='search'),
]

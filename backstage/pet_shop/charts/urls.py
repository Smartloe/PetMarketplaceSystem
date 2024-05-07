# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/7 18:30
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/7 18:30
@Description: 
"""
from django.urls import path
from . import views

urlpatterns = [
	path('chart_data/', views.chart_data, name='chart_data'),
]

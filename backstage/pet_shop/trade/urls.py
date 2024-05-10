# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/9 23:36
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/9 23:36
@Description: 
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderInfosViewSet, OrderGoodsViewSet, ShoppingCartViewSet

router = DefaultRouter()
router.register(r'orders', OrderInfosViewSet, basename='orders')
router.register(r'order-goods', OrderGoodsViewSet, basename='order-goods')
router.register(r'shopping-carts', ShoppingCartViewSet, basename='shopping-carts')

urlpatterns = [
	path('', include(router.urls)),
]

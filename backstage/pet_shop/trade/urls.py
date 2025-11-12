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
from .api_views import CheckoutView, OrderRefundView, ConfirmReceiptView, OrderGoodsCommentView

router = DefaultRouter()
router.register(r'orders', OrderInfosViewSet, basename='orders')
router.register(r'order-goods', OrderGoodsViewSet, basename='order-goods')
router.register(r'shopping-carts', ShoppingCartViewSet, basename='shopping-carts')

urlpatterns = [
	path('', include(router.urls)),
	path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('orders/<int:order_id>/refund/', OrderRefundView.as_view(), name='order-refund'),
	path('orders/<int:order_id>/confirm/', ConfirmReceiptView.as_view(), name='order-confirm'),
	path('orders/<int:order_id>/goods/<int:order_goods_id>/comment/', OrderGoodsCommentView.as_view(), name='order-goods-comment'),
]

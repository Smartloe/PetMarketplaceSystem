# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/9 23:39
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/9 23:39
@Description: 
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'favorites', UserFavViewSet, basename='user-favorites')
router.register(r'messages', UserLeavingMessageViewSet, basename='user-messages')
router.register(r'addresses', UserAddressViewSet, basename='user-addresses')
router.register(r'usercomments', UserCommentViewSet, basename='user-comments')

urlpatterns = [
	path('', include(router.urls)),
	path('regions/', RegionListView.as_view(), name='region-list'),
]

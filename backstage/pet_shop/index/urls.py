# -*- coding: utf-8 -*-
"""
Index app URL configuration.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AIPetConsultView, ConsultSessionViewSet

router = DefaultRouter()
# GET /ai/sessions/            列表
# GET /ai/sessions/<pk>/       详情
# DELETE /ai/sessions/<pk>/    删除（原先是 /ai/sessions/<pk>/delete/）
router.register('ai/sessions', ConsultSessionViewSet, basename='ai-session')

urlpatterns = [
	path('ai/consult/', AIPetConsultView.as_view(), name='ai-pet-consult'),
	path('', include(router.urls)),
]

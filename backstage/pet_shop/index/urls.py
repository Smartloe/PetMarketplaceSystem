# -*- coding: utf-8 -*-
"""
Index app URL configuration.
"""
from django.urls import path

from .views import (
	AIPetConsultView,
	ConsultSessionDeleteView,
	ConsultSessionDetailView,
	ConsultSessionListView,
)

urlpatterns = [
	path('ai/consult/', AIPetConsultView.as_view(), name='ai-pet-consult'),
	path('ai/sessions/', ConsultSessionListView.as_view(), name='ai-session-list'),
	path('ai/sessions/<int:session_id>/', ConsultSessionDetailView.as_view(), name='ai-session-detail'),
	path('ai/sessions/<int:session_id>/delete/', ConsultSessionDeleteView.as_view(), name='ai-session-delete'),
]

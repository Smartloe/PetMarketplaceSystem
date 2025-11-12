# -*- coding: utf-8 -*-
"""
Index app URL configuration.
"""
from django.urls import path

from .views import AIPetConsultView

urlpatterns = [
	path('ai/consult/', AIPetConsultView.as_view(), name='ai-pet-consult'),
]

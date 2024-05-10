# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvertisementViewSet

router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet, basename='advertisements')

urlpatterns = [
	path('', include(router.urls)),
]

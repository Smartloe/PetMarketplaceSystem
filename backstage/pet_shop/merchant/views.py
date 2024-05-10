from rest_framework import viewsets
from .models import Advertisement
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Advertisement.objects.all()
	serializer_class = AdvertisementSerializer

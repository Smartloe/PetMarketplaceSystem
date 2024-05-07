from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


# Create your views here.
class commodityView(APIView):
	'''
	商品列表页
	'''
	authentication_classes = []
	permission_classes = []

	def get(self, request):
		# 获取商品分类信息
		types = CommodityCategories.objects.all()
		# 获取商品信息
		commodity_infos = CommodityInfos.objects.all()
		# 序列化
		types_serializer = TypesSerializer(types, many=True)
		commodity_infos_serializer = CommodityInfosSerializer(commodity_infos, many=True)
		return Response({
			'types': types_serializer.data,
			'commodity_infos': commodity_infos_serializer.data
		})

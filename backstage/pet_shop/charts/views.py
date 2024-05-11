from django.http import JsonResponse
from echarts import Echart, Legend, Bar
from commodity.models import *


# Create your views here.
def sold_data(request):
	chart = Echart('商品销量TOP10', '吉祥宠物商城销量前十的商品')
	chart.use(Bar('China', [2, 3, 4, 5]))
	chart.use(Legend(['GDP']))
	return JsonResponse(chart.json)

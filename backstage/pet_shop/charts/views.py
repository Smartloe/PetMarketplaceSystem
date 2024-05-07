from django.http import JsonResponse
from echarts import Echart, Legend, Bar


def chart_data(request):
	chart = Echart('GDP', 'This is a fake chart')
	chart.use(Bar('China', [2, 3, 4, 5]))
	chart.use(Legend(['GDP']))
	return JsonResponse(chart.json)

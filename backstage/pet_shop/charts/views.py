from django.http import JsonResponse
from django.shortcuts import render
from commodity.models import CommodityInfos


def sold_view(request):
	# 获取销量最高的10个商品
	top_commodities = CommodityInfos.objects.all().order_by('-sold')[:10]

	# 准备图表数据
	chart_data = {
		'title': {'text': 'Top 10 商品销量'},
		'tooltip': {},
		'legend': {'data': ['销量']},
		'xAxis': {
			'type': 'category',
			'data': [commodity.name for commodity in top_commodities]
		},
		'yAxis': {'type': 'value'},
		'series': [{
			'name': '销量',
			'type': 'bar',
			'data': [commodity.sold for commodity in top_commodities]
		}]
	}

	# 将图表数据传递给模板
	context = {
		'chart_data': chart_data,
		'opts': CommodityInfos._meta,
		'has_change_permission': True,  # 或者使用权限检查
	}
	return JsonResponse(chart_data)

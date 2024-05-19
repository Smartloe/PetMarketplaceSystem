from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import *
from rest_framework.generics import ListAPIView
from customer_operation.models import UserComment


# Create your views here.
class commodityView(APIView):
	'''
	商品列表页
	'''
	authentication_classes = []
	permission_classes = []

	def get(self, request):
		# 获取所有商品类型
		categories = CommodityCategories.objects.all()

		# 初始化一个字典来存储商品数据
		data = {}

		# 遍历所有商品类型
		for category in categories:
			# 判断当前类型是否有父类型
			if category.parent_category:
				# 如果有父类型,将商品数据添加到父类型下
				parent_category_title = category.parent_category.title
				if parent_category_title not in data:
					data[parent_category_title] = {
						'sub_categories': [],
						# 'commodities': []
					}
				data[parent_category_title]['sub_categories'].append({
					'title': category.title,
					'commodities': []
				})
			else:
				# 如果没有父类型,将商品数据添加到顶级类型下
				if category.title not in data:
					data[category.title] = {
						'sub_categories': [],
						# 'commodities': []
					}

			# 获取该类型下的所有商品
			commodities = CommodityInfos.objects.filter(types=category)

			# 序列化商品信息
			commodities_serializer = CommodityInfosSerializer(commodities, many=True)

			# 将该类型的商品信息添加到对应的位置
			if category.parent_category:
				parent_category_title = category.parent_category.title
				for sub_category in data[parent_category_title]['sub_categories']:
					if sub_category['title'] == category.title:
						sub_category['commodities'] = commodities_serializer.data
						break
		# else:
		# 	data[category.title]['commodities'] = commodities_serializer.data

		return Response(data)


class detailView(APIView):
	'''
	商品详情页
	'''
	authentication_classes = []
	permission_classes = []

	def get(self, request, pk):
		try:
			# 获取商品信息
			commodity_info = CommodityInfos.objects.get(id=pk)
		except CommodityInfos.DoesNotExist:
			return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)

		# 序列化商品信息
		commodity_info_serializer = CommodityInfosSerializer(commodity_info)

		# 获取该商品所属的类型信息
		commodity_category = commodity_info.types
		category_serializer = TypesSerializer(commodity_category)

		# 构建响应数据
		data = {
			'category': category_serializer.data,
			'commodity_info': commodity_info_serializer.data,
		}

		return Response(data)


class CommoditySearchView(APIView):
	'''
	商品搜索
	'''
	authentication_classes = []
	permission_classes = []

	def get(self, request):
		# 从请求参数中获取搜索关键字
		query = request.GET.get('query', '')

		# 使用Q对象进行模糊查询
		commodities = CommodityInfos.objects.filter(
			Q(sku_title__icontains=query) | Q(sku_description__icontains=query)
		)

		# 序列化查询结果
		serializer = CommodityInfosSerializer(commodities, many=True)

		# 返回查询结果
		return Response(serializer.data)


class CommodityCommentsView(ListAPIView):
	"""
	商品评论列表
	"""
	serializer_class = GoodsCommentSerializer

	def get_queryset(self):
		"""
		重写get_queryset方法来返回一个商品的所有评论
		"""
		commodity_id = self.kwargs['pk']  # 从URL捕获的商品ID
		return UserComment.objects.filter(commodity__id=commodity_id, is_show=True)

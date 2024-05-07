# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/1 15:00
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/1 15:00
@Description: 
"""
from rest_framework.views import APIView


class commodityView(APIView):
	'''
	商品列表页
	'''
	pass


class detailView(APIView):
	'''
	商品详情页
	'''
	authentication_classes = []
	permission_classes = []


class collectView(APIView):
	'''
	商品收藏
	'''
	authentication_classes = []
	permission_classes = []

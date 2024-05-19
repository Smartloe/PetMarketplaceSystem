# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/6 11:16
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/6 11:16
@Description: 
"""
from rest_framework import serializers
from .models import *
from customer_operation.models import UserComment as CommodityUserComment


# 定义ModelSerializer类
class TypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommodityCategories
		fields = '__all__'


class CommodityInfosSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommodityInfos
		fields = '__all__'


class GoodsCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommodityUserComment
		fields = '__all__'  # 或者指定需要序列化的字段列表

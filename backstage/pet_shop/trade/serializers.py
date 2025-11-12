# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/10 14:47
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/10 14:47
@Description: 
"""
from rest_framework import serializers
from .models import OrderInfos, OrderGoods, ShoppingCart


class OrderGoodsSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderGoods
		fields = '__all__'


class OrderInfosSerializer(serializers.ModelSerializer):
	goods = OrderGoodsSerializer(many=True, read_only=True)

	class Meta:
		model = OrderInfos
		fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = ShoppingCart
		fields = '__all__'

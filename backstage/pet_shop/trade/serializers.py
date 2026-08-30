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
		# 订单商品行只随结算/评价流程维护，禁止客户端直接写。
		read_only_fields = ['order', 'goods', 'goods_num', 'commented']


class OrderInfosSerializer(serializers.ModelSerializer):
	goods = OrderGoodsSerializer(many=True, read_only=True)

	class Meta:
		model = OrderInfos
		fields = '__all__'
		# 金额与状态只能由 checkout / pay / refund / confirm 等专用端点
		# 按状态机流转。此前全字段可写，客户端可以直接 PUT 把订单改成
		# “已签收”或篡改应付金额。
		read_only_fields = [
			'user', 'order_sn', 'address', 'total_price', 'coupon_price',
			'payable_price', 'pay_method', 'leave_comment', 'order_status',
			'confirmed_time', 'refund_status', 'refund_reason',
			'created_by', 'update_by',
		]


class ShoppingCartSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = ShoppingCart
		fields = '__all__'
		extra_kwargs = {
			# 数量至少为 1，防止通过 PUT 塞进 0 或负数
			'quantity': {'min_value': 1},
		}

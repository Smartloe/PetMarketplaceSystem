# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/10 1:12
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/10 1:12
@Description: 
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from pet_shop.regions import get_region_helper


class UserFavSerializer(serializers.ModelSerializer):
	"""
	用户收藏序列化器
	"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = UserFav
		fields = "__all__"


class UserLeavingMessageSerializer(serializers.ModelSerializer):
	"""
	用户留言序列化器
	"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = UserLeavingMessage
		fields = "__all__"
		# 客服回复只能由后台维护。此前客户端可以自带 is_replied /
		# reply_content 伪造出“已回复”。
		read_only_fields = ['is_replied', 'reply_content', 'reply_time']


class UserAddressSerializer(serializers.ModelSerializer):
	"""
	用户地址序列化器
	"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = UserAddress
		fields = "__all__"
		# 经手人由服务端记录，不接受客户端申报
		read_only_fields = ['created_by', 'updated_by']

	def validate(self, attrs):
		province = attrs.get('province')
		city = attrs.get('city')
		county = attrs.get('county')
		try:
			get_region_helper().validate(province, city, county)
		except ValueError as exc:
			raise serializers.ValidationError({'region': str(exc)})
		return super().validate(attrs)


class UserCommentSerializer(serializers.ModelSerializer):
	"""
	用户评论序列化器（只作展示输出）。评论的创建只随“确认收货后
	评价”的 trade.OrderGoodsCommentView 发生；is_show 审核开关
	只归后台管理，此前客户端可自带 is_show=True 绕过审核。
	"""

	class Meta:
		model = UserComment
		fields = '__all__'
		read_only_fields = ['user', 'commodity', 'content', 'rating', 'is_show', 'created_by']

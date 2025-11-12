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


class UserAddressSerializer(serializers.ModelSerializer):
	"""
	用户地址序列化器
	"""
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = UserAddress
		fields = "__all__"

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
		用户评论序列化器
		"""

	class Meta:
		model = UserComment
		fields = '__all__'

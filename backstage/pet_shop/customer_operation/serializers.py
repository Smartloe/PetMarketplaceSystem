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


class UserCommentSerializer(serializers.ModelSerializer):
	"""
		用户评论序列化器
		"""

	class Meta:
		model = UserComment
		fields = '__all__'

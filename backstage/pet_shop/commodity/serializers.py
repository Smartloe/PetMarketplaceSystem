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
from accounts.models import UserProfile  # 确保导入UserProfile模型


# 定义ModelSerializer类
class TypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommodityCategories
		fields = '__all__'


class CommodityInfosSerializer(serializers.ModelSerializer):
	"""
	商品输出（列表/详情/搜索对匿名访客开放）。必须显式列出字段：
	进价 cost_price 与经手人 created_by/updated_by 是内部数据，
	此前随 '__all__' 泄漏给了所有访客。
	"""

	class Meta:
		model = CommodityInfos
		fields = [
			'id', 'sku_title', 'sku_description', 'main_image',
			'detail_images', 'price', 'status', 'types',
			'sold', 'stock_quantity', 'created_time', 'updated_time',
		]


class GoodsCommentSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField()
	avatar = serializers.SerializerMethodField()

	class Meta:
		model = CommodityUserComment
		fields = ['id', 'content', 'rating', 'created_time', 'username', 'avatar']  # 指定需要序列化的字段

	def get_username(self, obj):
		return obj.user.username

	def get_avatar(self, obj):
		# 获取UserProfile实例
		user_profile = UserProfile.objects.filter(username=obj.user).first()
		if user_profile and user_profile.avatar:
			# 返回头像的路径
			return user_profile.avatar.url
		else:
			# 如果没有头像或UserProfile不存在，返回默认头像的路径
			return 'media/profile_photos/default.png'

# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/6 11:16
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/6 11:16
@Description:
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
	"""
	注册序列化器,只包含username、email、password和password2字段
	"""
	password2 = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def validate(self, attrs):
		"""
		验证密码和确认密码是否一致,以及邮箱是否已被注册
		"""
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError("密码和确认密码不一致")
		attrs.pop('password2')
		email = attrs['email']
		if User.objects.filter(email=email).exists():
			raise serializers.ValidationError("邮箱已被注册")
		return attrs

	def create(self, validated_data):
		"""
		创建用户,将密码加密后存入数据库
		"""
		validated_data['password'] = make_password(validated_data['password'])
		return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
	"""
	登录序列化器,包含username、password和code字段
	"""
	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True, write_only=True)
	code = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
	"""
	用户信息序列化器
	"""
	username = serializers.CharField(source='username.username', read_only=True)

	class Meta:
		model = UserProfile
		fields = (
			'id', 'username', 'birthday', 'gender', 'user_intro', 'avatar', 'mobile', 'user_score', 'total_cost_amt',
			'updated_time')

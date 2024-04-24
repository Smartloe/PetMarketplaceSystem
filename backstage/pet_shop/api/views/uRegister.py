# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/4/24 17:11
@Last Modified by:   Chenxr
@Last Modified time: 2024/4/24 17:13:49
@Description: 用户注册
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import RegisterSerializers
from api.models import UserInfo


class UserRegister(APIView):
	def post(self, request):
		ser = RegisterSerializers(data=request.data)
		# 先进行常规数据验证
		if not ser.is_valid():
			return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "用户注册失败", "details": ser.errors})
		# 邮箱唯一性检查
		email = ser.validated_data['email']
		if UserInfo.objects.filter(email=email).exists():  # 检查数据库中是否存在相同邮箱的用户
			ser._errors['email'] = ['该邮箱已存在，请使用其他邮箱进行注册']  # 添加错误信息到序列化器的错误字典
		ser = RegisterSerializers(data=request.data)
		# 先进行常规数据验证
		if not ser.is_valid():
			return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "用户注册失败", "details": ser.errors})
		# 邮箱唯一性检查
		email = ser.validated_data['email']
		if UserInfo.objects.filter(email=email).exists():  # 检查数据库中是否存在相同邮箱的用户
			ser._errors['email'] = ['该邮箱已存在，请使用其他邮箱进行注册']  # 添加错误信息到序列化器的错误字典
			return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "用户注册失败", "details": ser.errors})
		# 邮箱未存在，继续注册流程
		ser.validated_data.pop('confirm_password')
		ser.save()
		return Response({"status": status.HTTP_201_CREATED, 'message': '用户注册成功', "details": ser.data})

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
from api.models import UserInfos

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import RegisterSerializers


class UserRegister(APIView):
	def post(self, request):
		ser = RegisterSerializers(data=request.data)
		if ser.is_valid():
			user = ser.save()
			return Response({
				"status": status.HTTP_201_CREATED,
				'message': '用户注册成功',
				"details": {
					'id': user.id,
					'nick_name': user.nick_name,
					'email': user.email
				}
			})
		else:
			return Response({
				"status": status.HTTP_400_BAD_REQUEST,
				"message": "用户注册失败",
				"details": ser.errors
			})

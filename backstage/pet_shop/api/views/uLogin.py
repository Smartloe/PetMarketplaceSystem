# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/4/24 17:11
@Last Modified by:   Chenxr
@Last Modified time: 2024/4/24 17:13:49
@Description: 用户登录
"""
import uuid
import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import LoginSerializers
from api.models import UserInfo
from datetime import datetime


class UserLogin(APIView):

	def post(self, request):
		ser = LoginSerializers(data=request.data)
		if not ser.is_valid():
			return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "用户登录失败", "details": ser.errors})

		instance = UserInfo.objects.filter(**ser.validated_data).first()
		if not instance:
			return Response(
				{"status": status.HTTP_400_BAD_REQUEST, "message": "用户登录失败", "details": "用户名或密码错误"})
		token = str(uuid.uuid4().hex)
		instance.token = token
		# 获取当前的UTC时间
		utc_time = datetime.now(pytz.utc)
		# 设置北京时区
		beijing_tz = pytz.timezone('Asia/Shanghai')
		# 将UTC时间转换为北京时间
		beijing_time = utc_time.astimezone(beijing_tz)
		instance.last_login_time = beijing_time
		instance.save()
		return Response(
			{
				"status": status.HTTP_200_OK,
				"message": "用户登录成功",
				"details":
					{
						'nickname': instance.nick_name,
						'token': instance.token,
						'login_time': instance.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
					}
			}
		)
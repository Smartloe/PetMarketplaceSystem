# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/4/24 17:11
@Last Modified by:   Chenxr
@Last Modified time: 2024/4/24 17:13:49
@Description: 用户登录
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import LoginSerializers
from rest_framework.authtoken.models import Token
from datetime import datetime
import pytz


class UserLogin(APIView):

	def post(self, request):
		ser = LoginSerializers(data=request.data)
		if not ser.is_valid():
			return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

		user = ser.validated_data
		token, created = Token.objects.get_or_create(user=user)

		# 获取当前的UTC时间
		utc_time = datetime.now(pytz.utc)
		# 设置北京时区
		beijing_tz = pytz.timezone('Asia/Shanghai')
		# 将UTC时间转换为北京时间
		beijing_time = utc_time.astimezone(beijing_tz)
		user.last_login_time = beijing_time
		user.save()
		return Response(
			{
				"status": status.HTTP_200_OK,
				"message": "用户登录成功",
				"details":
					{
						'nickname': user.nick_name,
						'token': token.key,
						'login_time': user.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
					}
			},
			status=status.HTTP_200_OK
		)

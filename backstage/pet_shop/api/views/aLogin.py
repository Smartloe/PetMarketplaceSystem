# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/4/24 17:11
@Last Modified by:   Chenxr
@Last Modified time: 2024/4/24 17:11
@Description: 管理员登录
"""
import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import AdminLoginSerializers
from api.models import Admin
from datetime import datetime


class AdminLogin(APIView):
	def post(self, request):
		ser = AdminLoginSerializers(data=request.data)
		if not ser.is_valid():
			return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "管理员登录失败", "details": ser.errors})
		instance = Admin.objects.filter(**ser.validated_data).first()
		if not instance:
			return Response(
				{"status": status.HTTP_400_BAD_REQUEST, "message": "管理员登录失败", "details": "用户名或密码错误"})
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
				"message": "管理员登录成功",
				"details": {
					'username': instance.username,
					'phone_number': instance.phone_number,
					'login_time': instance.last_login_time.strftime('%Y-%m-%d %H:%M:%S')
				}
			},
		)

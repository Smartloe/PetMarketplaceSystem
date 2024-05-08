from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authtoken.models import Token
from datetime import datetime
import pytz


# Create your views here.
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

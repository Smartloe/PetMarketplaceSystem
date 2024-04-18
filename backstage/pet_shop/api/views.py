import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializers, LoginSerializers
from .models import UserInfo


# Create your views here.
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
        instance.save()
        return Response({"status": status.HTTP_200_OK, "message": "用户登录成功",
                         "details": {'username': instance.username, 'token': instance.token}})

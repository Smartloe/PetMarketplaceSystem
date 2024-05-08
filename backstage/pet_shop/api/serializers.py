from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class RegisterSerializers(serializers.ModelSerializer):
	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = UserInfos
		fields = ['id', 'nick_name', 'email', 'password', 'confirm_password']
		extra_kwargs = {
			'id': {
				'read_only': True
			},
			'password': {
				'write_only': True,
				'style': {'input_type': 'password'}
			}
		}

	def validate_email(self, value):
		if UserInfos.objects.filter(email=value).exists():
			raise serializers.ValidationError("该邮箱已存在，请使用其他邮箱进行注册")
		return value

	def validate(self, data):
		if data['password'] != data.pop('confirm_password'):
			raise serializers.ValidationError("两次输入的密码不一致")
		data['password'] = make_password(data['password'])
		return data

	def create(self, validated_data):
		user = UserInfos.objects.create(**validated_data)
		return user


class LoginSerializers(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(style={'input_type': 'password'})

	def validate(self, data):
		user = authenticate(email=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError("无法登录，邮箱或密码不正确")
		return user

	def create(self, validated_data):
		token, created = Token.objects.get_or_create(user=validated_data)
		return token.key


class AdminLoginSerializers(serializers.ModelSerializer):
	class Meta:
		model = Admin
		fields = ['username', 'password']


class CommodityInfosSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommodityInfos
		fields = '__all__'


class TypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategories
		fields = '__all__'

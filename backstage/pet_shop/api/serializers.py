from rest_framework import serializers
from .models import UserInfo
from rest_framework import exceptions
from .utils.encrypt import md5


class RegisterSerializers(serializers.ModelSerializer):
    """
    write_only=True参数意味着该字段仅在数据写入（如POST请求）时有效，但在响应数据（如GET请求）中不会返回。这样设计是为了在用户注册时要求输入确认密码以验证密码输入的一致性，但避免在返回的用户信息中暴露确认密码字段。
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_password(self, value):
        md5_hash = md5(value)
        return md5_hash

    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if password and password != value:
            raise exceptions.ValidationError('两次输入的密码不一致')
        return value


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['email', 'password']

    def validate_password(self, value):
        md5_hash = md5(value)
        return md5_hash

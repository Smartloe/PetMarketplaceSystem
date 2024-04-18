import hashlib
from django.conf import settings


def md5(s):
    if s is None:
        # 可以返回 None 或抛出异常
        # return None
        # 或者抛出异常:
        raise ValueError("输入值不能为空")
    # 密码盐是settings.py的SECRET_KEY
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(s.encode('utf-8'))
    return obj.hexdigest()

# -*- coding: utf-8 -*-
"""
@Author: Chenxr
@Date:   2024/5/10 23:37
@Last Modified by:   Chenxr
@Last Modified time: 2024/5/10 23:37
@Description: 
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	自定义权限类,确保只有对象的所有者才能编辑它
	"""

	def has_object_permission(self, request, view, obj):
		# 读取权限对所有人开放
		if request.method in permissions.SAFE_METHODS:
			return True

		# 写入权限只有对象所有者才能访问
		return obj.user == request.user

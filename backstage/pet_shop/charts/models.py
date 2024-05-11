from django.db import models


# Create your models here.
class SoldModel(models.Model):
	name = models.CharField(max_length=50, verbose_name='商品名称')

	class Meta:
		verbose_name = '商品数据可视化'
		verbose_name_plural = verbose_name


class UserModel(models.Model):
	name = models.CharField(max_length=50, verbose_name='用户名称')

	class Meta:
		verbose_name = '用户数据可视化'
		verbose_name_plural = verbose_name

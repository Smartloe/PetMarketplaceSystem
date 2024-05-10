from django.db import models


# Create your models here.

class SoldModel(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name = '商品销量'
		verbose_name_plural = '商品销量'

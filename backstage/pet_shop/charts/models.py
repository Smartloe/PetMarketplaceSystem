from django.db import models


# Create your models here.

class MyModel(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name = '营业额'
		verbose_name_plural = '营业额'

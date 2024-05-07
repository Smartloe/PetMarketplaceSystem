from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


# 广告信息表
class Advertisement(models.Model):
	ad_title = models.CharField(max_length=255, verbose_name='广告标题')
	ad_content = models.CharField(max_length=255, verbose_name='广告内容')
	ad_image = models.ImageField(verbose_name='广告图片', upload_to="ad_photos/")
	ad_link = models.CharField(max_length=255, verbose_name='广告链接')
	start_date = models.DateTimeField(verbose_name='广告开始时间', null=True, blank=True)
	end_date = models.DateTimeField(verbose_name='广告结束时间', null=True, blank=True)
	click_count = models.IntegerField(verbose_name='点击次数', default=0)
	created_by = models.CharField(max_length=255, null=True, verbose_name='创建人')
	created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_by = models.CharField(max_length=255, null=True, verbose_name='创建人')
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	class Meta:
		verbose_name = '广告信息'
		verbose_name_plural = '广告信息'

	def __str__(self):
		return self.ad_title

from django.db import models

# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
	username = models.ForeignKey('auth.User', to_field='username', on_delete=models.CASCADE, verbose_name='用户名')
	birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
	GENDER_CHOICES = [
		('M', '男'),
		('F', '女'),
		('O', '其他'),
	]
	gender = models.CharField(
		max_length=1, choices=GENDER_CHOICES, verbose_name="性别",
		null=True, blank=True,
	)  # 添加性别字段
	user_intro = models.CharField(
		max_length=900, verbose_name='个性签名',
		null=True, blank=True,
		default='这个人很懒，什么都没有留下...'
	)
	avatar = models.ImageField(
		verbose_name='头像图片',
		upload_to="profile_photos/",
		null=True, blank=True,
		default='profile_photos/default.png'
	)
	mobile = PhoneNumberField(region='CN', verbose_name='手机号', null=True, blank=True)
	user_score = models.PositiveIntegerField(verbose_name='用户打分', null=True, blank=True, default=80)
	total_cost_amt = models.DecimalField(
		max_digits=24, decimal_places=2,
		verbose_name='累计消费金额', null=True,
		blank=True, default=0.00
	)
	updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True, blank=True)

	def __str__(self):
		return "用户信息"

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'

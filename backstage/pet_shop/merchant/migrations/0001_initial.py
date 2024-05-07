# Generated by Django 5.0.4 on 2024-05-06 04:55

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='姓名')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='电话')),
                ('is_active', models.SmallIntegerField(choices=[(0, '未激活'), (1, '已激活')], default=1, verbose_name='管理员状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_admins', to='merchant.admin', verbose_name='创建人')),
            ],
            options={
                'verbose_name': '管理员信息',
                'verbose_name_plural': '管理员信息',
            },
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=255, verbose_name='广告标题')),
                ('ad_content', models.CharField(max_length=255, verbose_name='广告内容')),
                ('ad_image', models.ImageField(upload_to='ad_photos/', verbose_name='广告图片')),
                ('ad_link', models.CharField(max_length=255, verbose_name='广告链接')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='广告开始时间')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='广告结束时间')),
                ('click_count', models.IntegerField(default=0, verbose_name='点击次数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ads', to='customer.userinfos', verbose_name='创建人')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_ads', to='customer.userinfos', verbose_name='更新人')),
            ],
            options={
                'verbose_name': '广告信息',
                'verbose_name_plural': '广告信息',
            },
        ),
    ]
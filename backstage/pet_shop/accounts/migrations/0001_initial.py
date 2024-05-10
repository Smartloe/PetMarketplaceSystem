# Generated by Django 5.0.4 on 2024-05-10 21:26

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生年月')),
                ('gender', models.CharField(blank=True, choices=[('M', '男'), ('F', '女'), ('O', '其他')], max_length=1, null=True, verbose_name='性别')),
                ('user_intro', models.CharField(blank=True, default='这个人很懒，什么都没有留下...', max_length=900, null=True, verbose_name='个性签名')),
                ('avatar', models.ImageField(blank=True, default='profile_photos/default.png', null=True, upload_to='profile_photos/', verbose_name='头像图片')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='CN', verbose_name='手机号')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('user_status', models.SmallIntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='用户状态')),
                ('user_score', models.PositiveIntegerField(blank=True, default=80, null=True, verbose_name='用户打分')),
                ('total_cost_amt', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=24, null=True, verbose_name='累计消费金额')),
                ('updated_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]

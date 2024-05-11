# Generated by Django 5.0.4 on 2024-05-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
            ],
            options={
                'verbose_name': '商品数据可视化',
                'verbose_name_plural': '商品数据可视化',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='用户名称')),
            ],
            options={
                'verbose_name': '用户数据可视化',
                'verbose_name_plural': '用户数据可视化',
            },
        ),
    ]

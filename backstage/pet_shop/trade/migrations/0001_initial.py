# Generated by Django 5.0.4 on 2024-05-08 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commodity', '0002_initial'),
        ('customer', '0003_remove_orderinfos_address_remove_orderinfos_user_and_more'),
        ('customer_operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='购买数量')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('commodityInfos', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commodity.commodityinfos', verbose_name='商品信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.userinfos', verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
            },
        ),
        migrations.CreateModel(
            name='OrderInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='订单号')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=24, verbose_name='总金额')),
                ('coupon_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=24, null=True, verbose_name='优惠金额')),
                ('payable_price', models.DecimalField(decimal_places=2, max_digits=24, verbose_name='应付金额')),
                ('pay_method', models.SmallIntegerField(blank=True, choices=[(1, '微信'), (2, '支付宝'), (3, '银联')], verbose_name='支付方式')),
                ('leave_comment', models.CharField(blank=True, max_length=1000, verbose_name='订单留言备注')),
                ('order_status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付'), (2, '发货中'), (3, '已签收'), (4, '退货中'), (5, '已退货')], verbose_name='订单状态')),
                ('created_by', models.CharField(max_length=255, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_by', models.CharField(blank=True, max_length=255, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_operation.useraddress', verbose_name='地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.userinfos', verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=0, verbose_name='商品数量')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.commodityinfos', verbose_name='商品')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='trade.orderinfos', verbose_name='订单信息')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
            },
        ),
    ]

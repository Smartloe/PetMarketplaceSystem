# Generated by Django 5.0.4 on 2024-04-24 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userinfos_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_name', models.CharField(max_length=255, verbose_name='地址名称')),
                ('seq_number', models.IntegerField(verbose_name='顺序号')),
                ('province', models.CharField(max_length=255, verbose_name='省')),
                ('city', models.CharField(max_length=255, verbose_name='市')),
                ('county', models.CharField(max_length=255, verbose_name='区')),
                ('street', models.CharField(max_length=255, verbose_name='街道')),
                ('last_detail', models.CharField(max_length=255, verbose_name='门牌号')),
                ('revision', models.IntegerField(verbose_name='乐观锁')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_by', models.CharField(blank=True, max_length=32, verbose_name='更新人')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, verbose_name='姓名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('phone_number', models.CharField(max_length=255, verbose_name='电话')),
                ('is_active', models.SmallIntegerField(choices=[(0, '未激活'), (1, '已激活')], default=1, verbose_name='管理员状态')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=255, verbose_name='广告标题')),
                ('ad_content', models.CharField(max_length=255, verbose_name='广告内容')),
                ('ad_image', models.CharField(max_length=1000, verbose_name='广告图片')),
                ('ad_link', models.CharField(max_length=255, verbose_name='广告链接')),
                ('ad_publish_time', models.DateTimeField(blank=True, null=True, verbose_name='广告投放时间')),
                ('revision', models.IntegerField(verbose_name='乐观锁')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_by', models.CharField(blank=True, max_length=32, verbose_name='更新人')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='总金额')),
                ('payable_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='应付金额')),
                ('cart_status', models.SmallIntegerField(choices=[(0, '待确认'), (1, '已确认')], verbose_name='购物车状态')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_by', models.CharField(blank=True, max_length=32, verbose_name='更新人')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.CharField(blank=True, max_length=32, verbose_name='商品ID')),
                ('sku_title', models.CharField(blank=True, max_length=90, verbose_name='商品标题')),
                ('sku_intro', models.CharField(blank=True, max_length=3000, verbose_name='商品介绍')),
                ('price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='原价')),
                ('sale_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='售价')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='总金额')),
                ('coupon_price', models.DecimalField(blank=True, decimal_places=6, max_digits=24, null=True, verbose_name='优惠金额')),
                ('payable_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='应付金额')),
                ('pay_method', models.SmallIntegerField(blank=True, choices=[(1, '微信'), (2, '支付宝'), (3, '银联')], verbose_name='支付方式')),
                ('leave_comment', models.CharField(blank=True, max_length=1000, verbose_name='订单留言备注')),
                ('order_status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付')], verbose_name='订单状态')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.address', verbose_name='地址')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart', verbose_name='购物车')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_title', models.CharField(max_length=255, verbose_name='商品名称')),
                ('sku_description', models.CharField(blank=True, max_length=255, verbose_name='商品描述')),
                ('main_image', models.CharField(blank=True, max_length=255, verbose_name='商品主图')),
                ('detail_images', models.CharField(blank=True, max_length=255, verbose_name='商品细节图')),
                ('cost_price', models.CharField(blank=True, max_length=255, verbose_name='商品进价')),
                ('price', models.CharField(max_length=255, verbose_name='商品售价')),
                ('status', models.CharField(default='1', max_length=32, verbose_name='商品状态')),
                ('stock_quantity', models.CharField(blank=True, max_length=255, verbose_name='库存数量')),
                ('created_by', models.CharField(max_length=32, verbose_name='创建人')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_by', models.CharField(blank=True, max_length=32, verbose_name='更新人')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='类别名称')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='详细描述')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(help_text='用户昵称', max_length=90, verbose_name='用户昵称')),
                ('user_intro', models.CharField(blank=True, help_text='个性签名', max_length=900, verbose_name='个性签名')),
                ('avatar', models.FileField(blank=True, help_text='头像图片', upload_to='profile_photo/', verbose_name='头像图片')),
                ('email', models.EmailField(help_text='邮件地址', max_length=254, verbose_name='邮件地址')),
                ('phone', models.CharField(blank=True, help_text='手机号', max_length=255, verbose_name='手机号')),
                ('user_pass', models.CharField(max_length=255, verbose_name='密码')),
                ('user_status', models.SmallIntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='用户状态')),
                ('token', models.CharField(blank=True, max_length=255, verbose_name='令牌')),
                ('user_score', models.IntegerField(blank=True, default='80', null=True, verbose_name='用户打分')),
                ('total_cost_amt', models.DecimalField(blank=True, decimal_places=6, max_digits=24, null=True, verbose_name='累计消费金额')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.DeleteModel(
            name='UserInfos',
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderinfo', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
    ]

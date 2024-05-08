# Generated by Django 5.0.4 on 2024-05-03 14:17

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_name', models.CharField(max_length=255, verbose_name='地址名称')),
                ('seq_number', models.PositiveIntegerField(verbose_name='顺序号')),
                ('province', models.CharField(max_length=255, verbose_name='省')),
                ('city', models.CharField(max_length=255, verbose_name='市')),
                ('county', models.CharField(max_length=255, verbose_name='区')),
                ('street', models.CharField(max_length=255, verbose_name='街道')),
                ('last_detail', models.CharField(max_length=255, verbose_name='门牌号')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否为默认地址')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '收货地址信息',
                'verbose_name_plural': '收货地址信息',
            },
        ),
        migrations.CreateModel(
            name='UserInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nick_name', models.CharField(help_text='用户昵称', max_length=90, verbose_name='用户昵称')),
                ('user_intro', models.CharField(blank=True, help_text='个性签名', max_length=900, verbose_name='个性签名')),
                ('avatar', models.ImageField(blank=True, help_text='头像图片', upload_to='profile_photos/', verbose_name='头像图片')),
                ('email', models.EmailField(help_text='邮件地址', max_length=254, verbose_name='邮件地址')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='手机号', max_length=128, region=None, verbose_name='手机号')),
                ('user_status', models.SmallIntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='用户状态')),
                ('token', models.CharField(blank=True, max_length=255, verbose_name='令牌')),
                ('user_score', models.PositiveIntegerField(blank=True, default=80, null=True, verbose_name='用户打分')),
                ('total_cost_amt', models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=24, null=True, verbose_name='累计消费金额')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
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
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_admins', to='api.admin', verbose_name='创建人')),
            ],
            options={
                'verbose_name': '管理员信息',
                'verbose_name_plural': '管理员信息',
            },
        ),
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='一级类型')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='api.productcategories', verbose_name='父级类型')),
            ],
            options={
                'verbose_name': '商品类型',
                'verbose_name_plural': '商品类型',
            },
        ),
        migrations.CreateModel(
            name='OrderInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='总金额')),
                ('coupon_price', models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=24, null=True, verbose_name='优惠金额')),
                ('payable_price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='应付金额')),
                ('pay_method', models.SmallIntegerField(blank=True, choices=[(1, '微信'), (2, '支付宝'), (3, '银联')], verbose_name='支付方式')),
                ('leave_comment', models.CharField(blank=True, max_length=1000, verbose_name='订单留言备注')),
                ('order_status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付'), (2, '发货中'), (3, '已签收'), (4, '退货中')], verbose_name='订单状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.address', verbose_name='地址')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_orders', to='api.userinfos', verbose_name='创建人')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.userinfos', verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='CommodityInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_title', models.CharField(max_length=255, verbose_name='商品名称')),
                ('sku_description', models.CharField(blank=True, max_length=255, verbose_name='商品描述')),
                ('main_image', models.ImageField(upload_to='product_photos/', verbose_name='商品主图')),
                ('detail_images', models.CharField(blank=True, max_length=255, verbose_name='商品细节图')),
                ('cost_price', models.DecimalField(blank=True, decimal_places=6, max_digits=24, verbose_name='商品进价')),
                ('price', models.DecimalField(decimal_places=6, max_digits=24, verbose_name='商品售价')),
                ('status', models.CharField(default='1', max_length=32, verbose_name='商品状态')),
                ('stock_quantity', models.PositiveIntegerField(blank=True, verbose_name='库存数量')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_commodities', to='api.userinfos', verbose_name='创建人')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_commodities', to='api.userinfos', verbose_name='更新人')),
            ],
            options={
                'verbose_name': '商品信息',
                'verbose_name_plural': '商品信息',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='购买数量')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('commodityInfos', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.commodityinfos', verbose_name='商品信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfos', verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
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
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ads', to='api.userinfos', verbose_name='创建人')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_ads', to='api.userinfos', verbose_name='更新人')),
            ],
            options={
                'verbose_name': '广告信息',
                'verbose_name_plural': '广告信息',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_addresses', to='api.userinfos', verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='address',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_addresses', to='api.userinfos', verbose_name='更新人'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='api.userinfos', verbose_name='用户'),
        ),
    ]

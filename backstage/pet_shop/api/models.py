from django.db import models


# Create your models here.


class UserInfo(models.Model):
    """用户信息表"""
    nick_name = models.CharField(max_length=90, verbose_name='用户昵称', help_text='用户昵称')
    user_intro = models.CharField(max_length=900, verbose_name='个性签名', blank=True, help_text='个性签名')
    # 本质上是数据库也是CharField,自动保存
    avatar = models.FileField(verbose_name='头像图片', upload_to="profile_photo/", blank=True, help_text='头像图片')
    email = models.EmailField(verbose_name='邮件地址', help_text='邮件地址')
    phone = models.CharField(max_length=255, verbose_name='手机号', blank=True, help_text='手机号')
    user_pass = models.CharField(max_length=255, verbose_name='密码')
    status_choices = (
        (0, "冻结"),
        (1, "正常"),
    )
    user_status = models.SmallIntegerField(max_length=4, default=1, verbose_name='用户状态', choices=status_choices, )
    token = models.CharField(max_length=255, verbose_name='令牌', blank=True)
    user_score = models.IntegerField(verbose_name='用户打分', null=True, blank=True, default='80')
    total_cost_amt = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='累计消费金额', null=True,
                                         blank=True)
    last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class OrderInfo(models.Model):
    """订单信息表"""
    user = models.ForeignKey(to='UserInfo', to_field="id", on_delete=models.CASCADE, verbose_name='用户')
    cart = models.ForeignKey(to='Cart', to_field="id", on_delete=models.CASCADE, verbose_name='购物车')
    address = models.ForeignKey(to='Address', to_field="id", on_delete=models.CASCADE, verbose_name='地址')
    total_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='总金额')
    coupon_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='优惠金额', null=True, blank=True)
    payable_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='应付金额')
    pay_choices = (
        (1, "微信"),
        (2, "支付宝"),
        (3, "银联"),
    )
    pay_method = models.SmallIntegerField(choices=pay_choices, verbose_name='支付方式', blank=True)
    leave_comment = models.CharField(max_length=1000, verbose_name='订单留言备注', blank=True)
    status_choices = (
        (0, "未支付"),
        (1, "已支付"),
    )
    order_status = models.SmallIntegerField(choices=status_choices, verbose_name='订单状态')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Cart(models.Model):
    """购物车信息表"""
    user = models.ForeignKey(to='UserInfo', to_field="id", on_delete=models.CASCADE, verbose_name='用户')
    total_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='总金额')
    payable_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='应付金额')
    status_choices = (
        (0, "待确认"),
        (1, "已确认"),
    )
    cart_status = models.SmallIntegerField(choices=status_choices, verbose_name='购物车状态')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=32, verbose_name='更新人', blank=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Item(models.Model):
    """购买明细表"""
    order = models.ForeignKey(to="OrderInfo", to_field="id", on_delete=models.CASCADE, verbose_name='订单')
    user = models.ForeignKey(to='UserInfo', to_field="id", on_delete=models.CASCADE, verbose_name='用户')

    sku_id = models.CharField(max_length=32, verbose_name='商品ID', blank=True)
    sku_title = models.CharField(max_length=90, verbose_name='商品标题', blank=True)
    sku_intro = models.CharField(max_length=3000, verbose_name='商品介绍', blank=True)
    price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='原价')
    sale_price = models.DecimalField(max_digits=24, decimal_places=6, verbose_name='售价')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Address(models.Model):
    """收货地址信息表"""
    address_name = models.CharField(max_length=255, verbose_name='地址名称')
    seq_number = models.IntegerField(verbose_name='顺序号')
    province = models.CharField(max_length=255, verbose_name='省')
    city = models.CharField(max_length=255, verbose_name='市')
    county = models.CharField(max_length=255, verbose_name='区')
    street = models.CharField(max_length=255, verbose_name='街道')
    last_detail = models.CharField(max_length=255, verbose_name='门牌号')
    revision = models.IntegerField(verbose_name='乐观锁')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=32, verbose_name='更新人', blank=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Advertisement(models.Model):
    """广告信息表"""
    ad_title = models.CharField(max_length=255, verbose_name='广告标题')
    ad_content = models.CharField(max_length=255, verbose_name='广告内容')
    ad_image = models.CharField(max_length=1000, verbose_name='广告图片')
    ad_link = models.CharField(max_length=255, verbose_name='广告链接')
    ad_publish_time = models.DateTimeField(verbose_name='广告投放时间', null=True, blank=True)
    revision = models.IntegerField(verbose_name='乐观锁')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=32, verbose_name='更新人', blank=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class Product(models.Model):
    """商品信息表"""
    sku_title = models.CharField(max_length=255, verbose_name='商品名称')
    sku_description = models.CharField(max_length=255, verbose_name='商品描述', blank=True)
    main_image = models.CharField(max_length=255, verbose_name='商品主图', blank=True)
    detail_images = models.CharField(max_length=255, verbose_name='商品细节图', blank=True)
    cost_price = models.CharField(max_length=255, verbose_name='商品进价', blank=True)
    price = models.CharField(max_length=255, verbose_name='商品售价')
    status = models.CharField(max_length=32, default='1', verbose_name='商品状态')
    stock_quantity = models.CharField(max_length=255, verbose_name='库存数量', blank=True)
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=32, verbose_name='更新人', blank=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class ProductCategories(models.Model):
    """商品分类信息表"""
    title = models.CharField(max_length=255, verbose_name='类别名称')
    description = models.CharField(max_length=255, verbose_name='详细描述', blank=True)


class Admin(models.Model):
    """管理员信息表"""
    username = models.CharField(max_length=255, verbose_name='姓名')
    password = models.CharField(max_length=255, verbose_name='密码')
    phone_number = models.CharField(max_length=255, verbose_name="电话")
    status_choices = (
        (0, "未激活"),
        (1, "已激活"),
    )
    is_active = models.SmallIntegerField(choices=status_choices, verbose_name='管理员状态')
    created_by = models.CharField(max_length=32, verbose_name='创建人')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

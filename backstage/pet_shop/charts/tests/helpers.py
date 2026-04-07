from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.utils import timezone

from commodity.models import CommodityCategories, CommodityInfos
from customer_operation.models import UserAddress, UserComment
from trade.models import OrderGoods, OrderInfos


def seed_minimal_order_scenario():
    now = timezone.now()

    food_category = CommodityCategories.objects.create(title="测试主粮")
    toy_category = CommodityCategories.objects.create(title="测试玩具")

    premium_food = CommodityInfos.objects.create(
        sku_title="高蛋白主粮",
        sku_description="测试数据：高单价主粮。",
        main_image="product_photos/test_main_1.png",
        detail_images="product_photos_details/test_detail_1.png",
        cost_price=Decimal("80.00"),
        price=Decimal("128.00"),
        status="1",
        types=food_category,
        sold=0,
        stock_quantity=20,
        created_by="test_seed",
        updated_by="test_seed",
    )
    low_stock_toy = CommodityInfos.objects.create(
        sku_title="磨牙玩具",
        sku_description="测试数据：低库存商品。",
        main_image="product_photos/test_main_2.png",
        detail_images="product_photos_details/test_detail_2.png",
        cost_price=Decimal("20.00"),
        price=Decimal("38.00"),
        status="1",
        types=toy_category,
        sold=0,
        stock_quantity=5,
        created_by="test_seed",
        updated_by="test_seed",
    )

    legacy_user = User.objects.create_user(username="legacy_buyer")
    new_user = User.objects.create_user(username="new_buyer")
    User.objects.filter(pk=legacy_user.pk).update(date_joined=now - timedelta(days=90))
    User.objects.filter(pk=new_user.pk).update(date_joined=now - timedelta(days=3))
    legacy_user.refresh_from_db()
    new_user.refresh_from_db()

    legacy_address = UserAddress.objects.create(
        user=legacy_user,
        province="浙江省",
        city="杭州市",
        county="西湖区",
        address="测试路 2 号",
        is_default=True,
        signer_name="老用户",
        signer_mobile="13800000002",
        created_by="test_seed",
        updated_by="test_seed",
    )
    new_address = UserAddress.objects.create(
        user=new_user,
        province="广东省",
        city="深圳市",
        county="南山区",
        address="测试路 1 号",
        is_default=True,
        signer_name="新用户",
        signer_mobile="13800000001",
        created_by="test_seed",
        updated_by="test_seed",
    )

    paid_order = OrderInfos.objects.create(
        user=new_user,
        order_sn="TEST-PAID-001",
        address=new_address,
        total_price=Decimal("138.00"),
        coupon_price=Decimal("10.00"),
        payable_price=Decimal("128.00"),
        pay_method=1,
        leave_comment="测试订单：已支付。",
        order_status=1,
        refund_status=0,
        created_by="test_seed",
        update_by="test_seed",
    )
    shipping_order = OrderInfos.objects.create(
        user=legacy_user,
        order_sn="TEST-SHIP-001",
        address=legacy_address,
        total_price=Decimal("76.00"),
        coupon_price=Decimal("0.00"),
        payable_price=Decimal("76.00"),
        pay_method=2,
        leave_comment="测试订单：发货中。",
        order_status=2,
        refund_status=2,
        created_by="test_seed",
        update_by="test_seed",
    )
    refunding_order = OrderInfos.objects.create(
        user=legacy_user,
        order_sn="TEST-REFUND-001",
        address=legacy_address,
        total_price=Decimal("38.00"),
        coupon_price=Decimal("0.00"),
        payable_price=Decimal("38.00"),
        pay_method=3,
        leave_comment="测试订单：退货中。",
        order_status=4,
        refund_status=1,
        refund_reason="测试售后",
        created_by="test_seed",
        update_by="test_seed",
    )
    unpaid_order = OrderInfos.objects.create(
        user=new_user,
        order_sn="TEST-UNPAID-001",
        address=new_address,
        total_price=Decimal("58.00"),
        coupon_price=Decimal("0.00"),
        payable_price=Decimal("58.00"),
        pay_method=1,
        leave_comment="测试订单：未支付。",
        order_status=0,
        refund_status=0,
        created_by="test_seed",
        update_by="test_seed",
    )

    OrderInfos.objects.filter(pk=paid_order.pk).update(
        created_time=now - timedelta(days=2),
        update_time=now - timedelta(days=2),
    )
    OrderInfos.objects.filter(pk=shipping_order.pk).update(
        created_time=now - timedelta(days=1),
        update_time=now - timedelta(days=1),
    )
    OrderInfos.objects.filter(pk=refunding_order.pk).update(
        created_time=now,
        update_time=now,
    )
    OrderInfos.objects.filter(pk=unpaid_order.pk).update(
        created_time=now - timedelta(days=1),
        update_time=now - timedelta(days=1),
    )
    paid_order.refresh_from_db()
    shipping_order.refresh_from_db()
    refunding_order.refresh_from_db()
    unpaid_order.refresh_from_db()

    paid_goods = OrderGoods.objects.create(
        order=paid_order,
        goods=premium_food,
        goods_num=1,
        commented=True,
    )
    shipping_goods = OrderGoods.objects.create(
        order=shipping_order,
        goods=low_stock_toy,
        goods_num=2,
        commented=False,
    )
    refunding_goods = OrderGoods.objects.create(
        order=refunding_order,
        goods=low_stock_toy,
        goods_num=1,
        commented=False,
    )
    unpaid_goods = OrderGoods.objects.create(
        order=unpaid_order,
        goods=premium_food,
        goods_num=1,
        commented=False,
    )
    OrderGoods.objects.filter(pk=paid_goods.pk).update(add_time=now - timedelta(days=2))
    OrderGoods.objects.filter(pk=shipping_goods.pk).update(add_time=now - timedelta(days=1))
    OrderGoods.objects.filter(pk=refunding_goods.pk).update(add_time=now)
    OrderGoods.objects.filter(pk=unpaid_goods.pk).update(add_time=now - timedelta(days=1))

    UserComment.objects.create(
        user=new_user,
        commodity=premium_food,
        content="评分很高的测试评论",
        rating=5,
        created_by="test_seed",
    )
    UserComment.objects.create(
        user=legacy_user,
        commodity=low_stock_toy,
        content="评分偏低的测试评论",
        rating=2,
        created_by="test_seed",
    )

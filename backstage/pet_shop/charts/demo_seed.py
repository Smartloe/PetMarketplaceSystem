from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone

from accounts.models import UserProfile
from charts.constants import (
    DEMO_CREATED_BY,
    DEMO_ORDER_PREFIX,
    DEMO_USER_PREFIX,
    LOW_STOCK_THRESHOLD,
)
from charts.demo_assets import DEMO_IMAGE_SOURCES
from commodity.models import CommodityCategories, CommodityInfos
from customer_operation.models import UserAddress, UserComment
from trade.models import OrderGoods, OrderInfos

DEMO_USER_COUNT = 24
DEMO_PRODUCT_COUNT = 30
DEMO_ORDERS_PER_USER = 4


@dataclass
class SeedSummary:
    users: int
    products: int
    orders: int


def _build_batch_id() -> str:
    return f"{timezone.now().strftime('%y%m%d%H%M%S')}{uuid4().hex[:4]}"


def _save_demo_media_file(target: str, source: Path | None) -> str:
    if source and source.exists():
        with source.open("rb") as source_file:
            return default_storage.save(target, File(source_file))
    return default_storage.save(target, ContentFile(b"demo-image"))


def _prepare_demo_images(batch_id: str) -> list[tuple[str, str]]:
    media_root = Path(settings.MEDIA_ROOT)
    (media_root / "product_photos").mkdir(parents=True, exist_ok=True)
    (media_root / "product_photos_details").mkdir(parents=True, exist_ok=True)

    image_pairs: list[tuple[str, str]] = []
    for index, source in enumerate(DEMO_IMAGE_SOURCES):
        filename = source.name if source.exists() else f"missing_{index}.png"
        main_image = _save_demo_media_file(
            f"product_photos/demo_{batch_id}_{index}_{filename}",
            source if source.exists() else None,
        )
        detail_image = _save_demo_media_file(
            f"product_photos_details/demo_{batch_id}_{index}_{filename}",
            source if source.exists() else None,
        )
        image_pairs.append((main_image, detail_image))

    if image_pairs:
        return image_pairs

    fallback_main = _save_demo_media_file(f"product_photos/demo_{batch_id}_fallback.png", None)
    fallback_detail = _save_demo_media_file(
        f"product_photos_details/demo_{batch_id}_fallback.png",
        None,
    )
    return [(fallback_main, fallback_detail)]


def _seed_categories() -> list[CommodityCategories]:
    categories: list[CommodityCategories] = []
    for title in ("主粮", "零食", "玩具", "护理", "出行"):
        category, _ = CommodityCategories.objects.get_or_create(
            title=title,
            defaults={"parent_category": None},
        )
        categories.append(category)
    return categories


def _seed_users_and_addresses(batch_id: str) -> tuple[list, list]:
    user_model = get_user_model()
    users = []
    addresses = []
    now = timezone.now()

    for index in range(DEMO_USER_COUNT):
        username = f"{DEMO_USER_PREFIX}_{batch_id}_{index:02d}"
        user = user_model.objects.create_user(
            username=username,
            password="DemoPass123!",
        )
        UserProfile.objects.create(
            username=user,
            gender="M" if index % 2 == 0 else "F",
            user_intro="演示账号，用于后台经营分析图表。",
            user_score=80 + (index % 20),
            total_cost_amt=Decimal("0.00"),
        )
        address = UserAddress.objects.create(
            user=user,
            province="广东省",
            city="深圳市",
            county="南山区",
            address=f"科技园路 {100 + index} 号",
            is_default=True,
            signer_name=f"演示用户{index + 1}",
            signer_mobile=f"1380000{index:04d}",
            created_by=DEMO_CREATED_BY,
            updated_by=DEMO_CREATED_BY,
        )

        created_at = now - timedelta(days=index % 30, hours=index % 24)
        UserAddress.objects.filter(pk=address.pk).update(
            created_time=created_at,
            updated_time=created_at,
        )

        users.append(user)
        addresses.append(address)

    return users, addresses


def _seed_products(
    batch_id: str,
    categories: list[CommodityCategories],
    image_pairs: list[tuple[str, str]],
) -> list[CommodityInfos]:
    products: list[CommodityInfos] = []
    now = timezone.now()

    for index in range(DEMO_PRODUCT_COUNT):
        main_image, detail_image = image_pairs[index % len(image_pairs)]
        category = categories[index % len(categories)]
        cost_price = Decimal("20.00") + Decimal(index % 12) * Decimal("3.50")
        price = cost_price + Decimal("15.00") + Decimal(index % 5) * Decimal("2.00")
        stock_quantity = max(1, LOW_STOCK_THRESHOLD + ((index % 9) - 4))

        product = CommodityInfos.objects.create(
            sku_title=f"演示商品-{batch_id}-{index + 1:02d}",
            sku_description="用于后台图表演示的数据商品。",
            main_image=main_image,
            detail_images=detail_image,
            cost_price=cost_price,
            price=price,
            status="1",
            types=category,
            sold=0,
            stock_quantity=stock_quantity,
            created_by=DEMO_CREATED_BY,
            updated_by=DEMO_CREATED_BY,
        )

        created_at = now - timedelta(days=index % 30, hours=(index * 2) % 24)
        CommodityInfos.objects.filter(pk=product.pk).update(
            created_time=created_at,
            updated_time=created_at + timedelta(hours=1),
        )
        products.append(product)

    return products


def _seed_orders_and_comments(
    batch_id: str,
    users: list,
    addresses: list[UserAddress],
    products: list[CommodityInfos],
) -> int:
    pay_methods = (1, 2, 3)
    order_statuses = (0, 1, 2, 3, 4, 5)
    sold_delta: dict[int, int] = {}
    orders_created = 0
    now = timezone.now()

    for user_index, (user, address) in enumerate(zip(users, addresses)):
        for offset in range(DEMO_ORDERS_PER_USER):
            sequence = user_index * DEMO_ORDERS_PER_USER + offset
            commodity = products[sequence % len(products)]
            goods_num = (offset % 3) + 1

            total_price = (commodity.price * goods_num).quantize(Decimal("0.01"))
            coupon_price = Decimal("5.00") if total_price >= Decimal("60.00") and offset % 2 == 0 else Decimal("0.00")
            payable_price = (total_price - coupon_price).quantize(Decimal("0.01"))

            order_status = order_statuses[sequence % len(order_statuses)]
            refund_status = 0
            refund_reason = ""
            if order_status in (4, 5):
                refund_status = (sequence % 3) + 1
                refund_reason = "演示订单售后退款"

            order = OrderInfos.objects.create(
                user=user,
                order_sn=f"{DEMO_ORDER_PREFIX}{batch_id}{sequence:04d}",
                address=address,
                total_price=total_price,
                coupon_price=coupon_price,
                payable_price=payable_price,
                pay_method=pay_methods[sequence % len(pay_methods)],
                leave_comment="演示订单，供后台图表统计使用。",
                order_status=order_status,
                refund_status=refund_status,
                refund_reason=refund_reason,
                created_by=DEMO_CREATED_BY,
                update_by=DEMO_CREATED_BY,
            )

            created_at = now - timedelta(days=sequence % 30, hours=(sequence * 3) % 24)
            confirmed_time = created_at + timedelta(hours=12) if order_status >= 3 else None
            OrderInfos.objects.filter(pk=order.pk).update(
                created_time=created_at,
                update_time=created_at + timedelta(hours=1),
                confirmed_time=confirmed_time,
            )

            order_goods = OrderGoods.objects.create(
                order=order,
                goods=commodity,
                goods_num=goods_num,
                commented=False,
            )

            if order_status >= 3 and sequence % 2 == 0:
                UserComment.objects.create(
                    user=user,
                    commodity=commodity,
                    content="演示评价：商品体验良好，物流速度快。",
                    rating=(sequence % 5) + 1,
                    created_by=DEMO_CREATED_BY,
                )
                order_goods.commented = True
                order_goods.save(update_fields=["commented"])

            sold_delta[commodity.pk] = sold_delta.get(commodity.pk, 0) + goods_num
            orders_created += 1

    if sold_delta:
        for product in products:
            increment = sold_delta.get(product.pk, 0)
            if increment:
                product.sold += increment
        CommodityInfos.objects.bulk_update(products, ["sold"])

    return orders_created


def seed_demo_business_data() -> SeedSummary:
    batch_id = _build_batch_id()
    with transaction.atomic():
        image_pairs = _prepare_demo_images(batch_id)
        categories = _seed_categories()
        users, addresses = _seed_users_and_addresses(batch_id)
        products = _seed_products(batch_id, categories, image_pairs)
        orders = _seed_orders_and_comments(batch_id, users, addresses, products)
        return SeedSummary(users=len(users), products=len(products), orders=orders)

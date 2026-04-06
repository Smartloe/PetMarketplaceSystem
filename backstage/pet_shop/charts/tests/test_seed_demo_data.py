from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from charts.constants import DEMO_USER_PREFIX
from commodity.models import CommodityInfos
from customer_operation.models import UserComment
from trade.models import OrderGoods, OrderInfos


class SeedDemoBusinessDataCommandTests(TestCase):
    def test_command_creates_demo_records_and_media_files(self):
        with TemporaryDirectory() as tmp_media:
            with override_settings(MEDIA_ROOT=tmp_media):
                call_command("seed_demo_business_data")
                call_command("seed_demo_business_data")

        products = CommodityInfos.objects.filter(created_by="demo_seed")
        product = products.first()
        self.assertIsNotNone(product)
        self.assertTrue(product.main_image.name.startswith("product_photos/"))
        self.assertTrue(product.detail_images.name.startswith("product_photos_details/"))
        self.assertGreater(OrderInfos.objects.filter(created_by="demo_seed").count(), 0)
        self.assertGreater(products.count(), 24)

        users = get_user_model().objects.filter(
            username__startswith=f"{DEMO_USER_PREFIX}_"
        ).order_by("date_joined")
        self.assertGreater(users.count(), 24)
        self.assertIsNotNone(users.first())
        self.assertIsNotNone(users.last())
        self.assertGreaterEqual(
            (users.last().date_joined - users.first().date_joined).days,
            20,
        )

        order_goods = OrderGoods.objects.filter(
            order__created_by="demo_seed"
        ).order_by("add_time")
        self.assertGreater(order_goods.count(), 0)
        self.assertIsNotNone(order_goods.first())
        self.assertIsNotNone(order_goods.last())
        self.assertGreaterEqual(
            (order_goods.last().add_time - order_goods.first().add_time).days,
            20,
        )

        comments = UserComment.objects.filter(created_by="demo_seed").order_by(
            "created_time"
        )
        self.assertGreater(comments.count(), 0)
        self.assertIsNotNone(comments.first())
        self.assertIsNotNone(comments.last())
        self.assertGreaterEqual(
            (comments.last().created_time - comments.first().created_time).days,
            20,
        )

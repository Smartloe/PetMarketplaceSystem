from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from charts.constants import DEMO_CREATED_BY, DEMO_USER_PREFIX
from commodity.models import CommodityInfos
from customer_operation.models import UserComment
from trade.models import OrderGoods, OrderInfos


class SeedDemoBusinessDataCommandTests(TestCase):
    def test_command_creates_demo_records_and_media_files(self):
        with TemporaryDirectory() as tmp_media:
            with override_settings(MEDIA_ROOT=tmp_media, DEBUG=True):
                call_command("seed_demo_business_data")
                call_command("seed_demo_business_data")

                products = CommodityInfos.objects.filter(
                    created_by=DEMO_CREATED_BY
                ).order_by("id")
                product = products.first()
                self.assertIsNotNone(product)
                self.assertTrue(product.main_image.name.startswith("product_photos/"))
                self.assertTrue(
                    product.detail_images.name.startswith("product_photos_details/")
                )
                self.assertTrue(Path(product.main_image.path).is_file())
                self.assertTrue(Path(product.detail_images.path).is_file())
                self.assertTrue(str(product.main_image.path).startswith(tmp_media))
                self.assertTrue(str(product.detail_images.path).startswith(tmp_media))
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
                for user in users:
                    self.assertFalse(user.has_usable_password())

                orders = OrderInfos.objects.filter(created_by=DEMO_CREATED_BY)
                self.assertGreater(orders.count(), 0)
                self.assertGreater(orders.values("order_status").distinct().count(), 1)
                self.assertSetEqual(
                    set(orders.values_list("pay_method", flat=True).distinct()),
                    {1, 2, 3},
                )
                self.assertSetEqual(
                    set(
                        orders.exclude(refund_status=0).values_list(
                            "refund_status",
                            flat=True,
                        )
                    ),
                    {1, 2, 3},
                )

                order_goods = OrderGoods.objects.filter(
                    order__created_by=DEMO_CREATED_BY
                ).order_by("add_time")
                self.assertGreater(order_goods.count(), 0)
                self.assertIsNotNone(order_goods.first())
                self.assertIsNotNone(order_goods.last())
                self.assertGreaterEqual(
                    (order_goods.last().add_time - order_goods.first().add_time).days,
                    20,
                )

                comments = UserComment.objects.filter(
                    created_by=DEMO_CREATED_BY
                ).order_by("created_time")
                self.assertGreater(comments.count(), 0)
                self.assertIsNotNone(comments.first())
                self.assertIsNotNone(comments.last())
                self.assertGreaterEqual(
                    (comments.last().created_time - comments.first().created_time).days,
                    20,
                )

    def test_command_refuses_to_run_when_debug_is_false(self):
        with override_settings(DEBUG=False):
            with self.assertRaisesMessage(
                CommandError,
                "seed_demo_business_data can only run when DEBUG=True.",
            ):
                call_command("seed_demo_business_data")

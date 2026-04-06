from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from charts.services import build_dashboard_payload, build_overview_payload
from charts.tests.helpers import seed_minimal_order_scenario
from customer_operation.models import UserAddress
from trade.models import OrderInfos


class AnalyticsServiceTests(TestCase):
    def test_overview_payload_uses_spec_metrics(self):
        seed_minimal_order_scenario()

        overview = build_overview_payload()
        self.assertIn("metrics", overview)
        self.assertIn("trends", overview)
        self.assertIn("category_share", overview)
        self.assertIn("hot_products", overview)
        self.assertIn("alerts", overview)

        self.assertEqual(overview["metrics"]["gmv"], "128.00")
        self.assertEqual(overview["metrics"]["low_stock_count"], 1)
        self.assertEqual(overview["metrics"]["new_users_count"], 1)
        self.assertEqual(overview["metrics"]["order_count"], 3)

        self.assertEqual(len(overview["trends"]["sales"]["7d"]), 7)
        self.assertEqual(len(overview["trends"]["sales"]["30d"]), 30)
        self.assertEqual(len(overview["trends"]["orders"]["7d"]), 7)
        self.assertEqual(len(overview["trends"]["orders"]["30d"]), 30)
        self.assertEqual(overview["trends"]["sales"]["7d"][0]["value"], 0)

        expected_start = (timezone.now().date() - timedelta(days=6)).strftime("%Y-%m-%d")
        self.assertEqual(overview["trends"]["sales"]["7d"][0]["date"], expected_start)
        self.assertSetEqual(
            set(overview["trends"]["sales"]["7d"][0].keys()),
            {"date", "value"},
        )

    def test_dashboard_payload_aggregates_sales_and_price_bands(self):
        seed_minimal_order_scenario()

        dashboard = build_dashboard_payload()
        self.assertIn("sections", dashboard)

        operations = dashboard["sections"]["operations"]
        self.assertEqual(operations["gmv"], "128.00")
        self.assertEqual(operations["order_count"], 3)
        self.assertEqual(operations["average_order_value"], "128.00")
        self.assertTrue(operations["payment_method_distribution"])
        self.assertSetEqual(
            set(operations["payment_method_distribution"][0].keys()),
            {"name", "value"},
        )

        catalog = dashboard["sections"]["catalog"]
        self.assertIn("category_share", catalog)
        self.assertIn("hot_products", catalog)
        self.assertIn("price_band_distribution", catalog)
        self.assertIn("low_stock_products", catalog)
        self.assertEqual(len(catalog["low_stock_products"]), 1)

        users = dashboard["sections"]["users"]
        self.assertEqual(len(users["new_user_trend"]["7d"]), 7)
        self.assertEqual(len(users["new_user_trend"]["30d"]), 30)
        self.assertTrue(users["province_distribution"])
        self.assertSetEqual(
            set(users["province_distribution"][0].keys()),
            {"name", "value"},
        )
        self.assertIn("rating_summary", users)

        orders = dashboard["sections"]["orders"]
        self.assertTrue(orders["status_distribution"])
        self.assertTrue(orders["refund_distribution"])
        self.assertEqual(len(orders["sales_trend"]["7d"]), 7)
        self.assertEqual(len(orders["sales_trend"]["30d"]), 30)
        self.assertEqual(len(orders["order_trend"]["7d"]), 7)
        self.assertEqual(len(orders["order_trend"]["30d"]), 30)

    def test_province_distribution_uses_order_address_counts(self):
        seed_minimal_order_scenario()

        dashboard = build_dashboard_payload()
        province_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["users"]["province_distribution"]
        }

        self.assertEqual(province_distribution["浙江省"], 2)
        self.assertEqual(province_distribution["广东省"], 1)

    def test_refund_distribution_uses_business_buckets(self):
        seed_minimal_order_scenario()
        now = timezone.now()

        base_user = User.objects.get(username="legacy_buyer")
        base_address = UserAddress.objects.filter(user=base_user).first()
        self.assertIsNotNone(base_address)

        returned_order = OrderInfos.objects.create(
            user=base_user,
            order_sn="TEST-RETURNED-001",
            address=base_address,
            total_price="88.00",
            coupon_price="0.00",
            payable_price="88.00",
            pay_method=1,
            leave_comment="测试订单：已退货",
            order_status=5,
            refund_status=0,
            created_by="test_seed",
            update_by="test_seed",
        )
        in_refund_order = OrderInfos.objects.create(
            user=base_user,
            order_sn="TEST-INREFUND-001",
            address=base_address,
            total_price="66.00",
            coupon_price="0.00",
            payable_price="66.00",
            pay_method=2,
            leave_comment="测试订单：退款中",
            order_status=4,
            refund_status=0,
            created_by="test_seed",
            update_by="test_seed",
        )
        OrderInfos.objects.filter(pk__in=[returned_order.pk, in_refund_order.pk]).update(
            created_time=now - timedelta(days=1),
            update_time=now - timedelta(days=1),
        )

        dashboard = build_dashboard_payload()
        refund_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["orders"]["refund_distribution"]
        }
        self.assertSetEqual(set(refund_distribution.keys()), {"退款中", "已退货"})
        self.assertEqual(refund_distribution["退款中"], 2)
        self.assertEqual(refund_distribution["已退货"], 2)

    def test_rolling_window_metrics_exclude_future_orders_and_users(self):
        seed_minimal_order_scenario()
        now = timezone.now()

        future_user = User.objects.create_user(username="future_buyer")
        User.objects.filter(pk=future_user.pk).update(date_joined=now + timedelta(days=2))
        future_user.refresh_from_db()

        future_address = UserAddress.objects.create(
            user=future_user,
            province="未来省",
            city="未来市",
            county="未来区",
            address="未来路 1 号",
            is_default=True,
            signer_name="未来用户",
            signer_mobile="13900000000",
            created_by="test_seed",
            updated_by="test_seed",
        )
        future_order = OrderInfos.objects.create(
            user=future_user,
            order_sn="TEST-FUTURE-001",
            address=future_address,
            total_price="999.00",
            coupon_price="0.00",
            payable_price="999.00",
            pay_method=1,
            leave_comment="未来订单，不应计入窗口统计",
            order_status=1,
            refund_status=0,
            created_by="test_seed",
            update_by="test_seed",
        )
        OrderInfos.objects.filter(pk=future_order.pk).update(
            created_time=now + timedelta(days=2),
            update_time=now + timedelta(days=2),
        )

        overview = build_overview_payload()
        dashboard = build_dashboard_payload()

        self.assertEqual(overview["metrics"]["gmv"], "128.00")
        self.assertEqual(overview["metrics"]["order_count"], 3)
        self.assertEqual(overview["metrics"]["new_users_count"], 1)
        self.assertEqual(dashboard["sections"]["operations"]["gmv"], "128.00")

        province_names = {
            item["name"]
            for item in dashboard["sections"]["users"]["province_distribution"]
        }
        self.assertNotIn("未来省", province_names)

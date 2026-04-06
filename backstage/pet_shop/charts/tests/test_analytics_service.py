from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from charts.services import build_dashboard_payload, build_overview_payload
from charts.tests.helpers import seed_minimal_order_scenario
from commodity.models import CommodityCategories, CommodityInfos
from customer_operation.models import UserAddress
from trade.models import OrderGoods, OrderInfos


class AnalyticsServiceTests(TestCase):
    def test_overview_payload_uses_spec_metrics(self):
        seed_minimal_order_scenario()

        self.assertEqual(OrderInfos.objects.count(), 4)
        overview = build_overview_payload()
        self.assertIn("metrics", overview)
        self.assertIn("trends", overview)
        self.assertIn("category_share", overview)
        self.assertIn("hot_products", overview)
        self.assertIn("alerts", overview)
        self.assertTrue(overview["category_share"])
        self.assertTrue(overview["hot_products"])
        self.assertTrue(overview["alerts"])
        self.assertSetEqual(
            set(overview["category_share"][0].keys()),
            {"name", "value"},
        )
        self.assertSetEqual(
            set(overview["hot_products"][0].keys()),
            {"product_id", "title", "sold_quantity", "stock_quantity"},
        )
        self.assertSetEqual(
            set(overview["alerts"][0].keys()),
            {"level", "title", "description", "target_url"},
        )

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
        self.assertTrue(catalog["category_share"])
        self.assertTrue(catalog["hot_products"])
        self.assertTrue(catalog["price_band_distribution"])
        self.assertEqual(len(catalog["low_stock_products"]), 1)
        self.assertSetEqual(
            set(catalog["category_share"][0].keys()),
            {"name", "value"},
        )
        self.assertSetEqual(
            set(catalog["hot_products"][0].keys()),
            {"product_id", "title", "sold_quantity", "stock_quantity"},
        )
        self.assertSetEqual(
            set(catalog["price_band_distribution"][0].keys()),
            {"name", "value"},
        )
        self.assertSetEqual(
            set(catalog["low_stock_products"][0].keys()),
            {"product_id", "title", "stock_quantity", "sold_quantity"},
        )

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
        self.assertSetEqual(
            set(orders["status_distribution"][0].keys()),
            {"name", "value"},
        )
        self.assertSetEqual(
            set(orders["refund_distribution"][0].keys()),
            {"name", "value"},
        )
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

    def test_refund_distribution_uses_order_status_precedence(self):
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
        overlap_order = OrderInfos.objects.create(
            user=base_user,
            order_sn="TEST-OVERLAP-001",
            address=base_address,
            total_price="77.00",
            coupon_price="0.00",
            payable_price="77.00",
            pay_method=2,
            leave_comment="测试订单：退款字段和状态重叠",
            order_status=4,
            refund_status=2,
            created_by="test_seed",
            update_by="test_seed",
        )
        OrderInfos.objects.filter(
            pk__in=[returned_order.pk, in_refund_order.pk, overlap_order.pk]
        ).update(
            created_time=now - timedelta(days=1),
            update_time=now - timedelta(days=1),
        )

        dashboard = build_dashboard_payload()
        refund_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["orders"]["refund_distribution"]
        }
        self.assertSetEqual(set(refund_distribution.keys()), {"退款中", "已退货"})
        self.assertEqual(refund_distribution["退款中"], 4)
        self.assertEqual(refund_distribution["已退货"], 1)
        self.assertEqual(
            refund_distribution["退款中"] + refund_distribution["已退货"],
            5,
        )
        self.assertGreater(refund_distribution["退款中"], refund_distribution["已退货"])

    def test_dashboard_distributions_and_top_lists_use_30d_window(self):
        seed_minimal_order_scenario()
        now = timezone.now()

        old_category = CommodityCategories.objects.create(title="历史分类")
        old_product = CommodityInfos.objects.create(
            sku_title="历史高销量商品",
            sku_description="超过30天的历史商品",
            main_image="product_photos/test_old_main.png",
            detail_images="product_photos_details/test_old_detail.png",
            cost_price=Decimal("50.00"),
            price=Decimal("520.00"),
            status="1",
            types=old_category,
            sold=0,
            stock_quantity=200,
            created_by="test_seed",
            updated_by="test_seed",
        )

        base_user = User.objects.get(username="legacy_buyer")
        old_address = UserAddress.objects.create(
            user=base_user,
            province="历史省",
            city="历史市",
            county="历史区",
            address="历史路 88 号",
            is_default=False,
            signer_name="历史用户",
            signer_mobile="13700000000",
            created_by="test_seed",
            updated_by="test_seed",
        )
        old_order = OrderInfos.objects.create(
            user=base_user,
            order_sn="TEST-OLD-001",
            address=old_address,
            total_price="520.00",
            coupon_price="0.00",
            payable_price="520.00",
            pay_method=1,
            leave_comment="超过30天的历史订单",
            order_status=5,
            refund_status=2,
            created_by="test_seed",
            update_by="test_seed",
        )
        OrderInfos.objects.filter(pk=old_order.pk).update(
            created_time=now - timedelta(days=45),
            update_time=now - timedelta(days=45),
        )
        OrderGoods.objects.create(
            order=old_order,
            goods=old_product,
            goods_num=99,
            commented=False,
        )

        overview = build_overview_payload()
        dashboard = build_dashboard_payload()

        overview_category_names = {item["name"] for item in overview["category_share"]}
        overview_hot_product_ids = {
            item["product_id"] for item in overview["hot_products"]
        }
        catalog_category_names = {
            item["name"] for item in dashboard["sections"]["catalog"]["category_share"]
        }
        catalog_hot_product_ids = {
            item["product_id"]
            for item in dashboard["sections"]["catalog"]["hot_products"]
        }
        province_names = {
            item["name"]
            for item in dashboard["sections"]["users"]["province_distribution"]
        }
        payment_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["operations"][
                "payment_method_distribution"
            ]
        }
        status_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["orders"]["status_distribution"]
        }
        refund_distribution = {
            item["name"]: item["value"]
            for item in dashboard["sections"]["orders"]["refund_distribution"]
        }

        self.assertNotIn("历史分类", overview_category_names)
        self.assertNotIn(old_product.id, overview_hot_product_ids)
        self.assertNotIn("历史分类", catalog_category_names)
        self.assertNotIn(old_product.id, catalog_hot_product_ids)
        self.assertNotIn("历史省", province_names)
        self.assertEqual(payment_distribution["微信"], 1)
        self.assertEqual(payment_distribution["支付宝"], 1)
        self.assertEqual(payment_distribution["银联"], 1)
        self.assertEqual(status_distribution["已退货"], 0)
        self.assertEqual(refund_distribution["退款中"], 2)
        self.assertEqual(refund_distribution["已退货"], 0)

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

        future_date = (now + timedelta(days=2)).date().strftime("%Y-%m-%d")
        sales_7d = overview["trends"]["sales"]["7d"]
        sales_30d = overview["trends"]["sales"]["30d"]
        order_7d = overview["trends"]["orders"]["7d"]
        order_30d = overview["trends"]["orders"]["30d"]
        user_7d = dashboard["sections"]["users"]["new_user_trend"]["7d"]
        user_30d = dashboard["sections"]["users"]["new_user_trend"]["30d"]

        self.assertNotIn(future_date, [item["date"] for item in sales_7d])
        self.assertNotIn(future_date, [item["date"] for item in sales_30d])
        self.assertNotIn(future_date, [item["date"] for item in order_7d])
        self.assertNotIn(future_date, [item["date"] for item in order_30d])
        self.assertNotIn(future_date, [item["date"] for item in user_7d])
        self.assertNotIn(future_date, [item["date"] for item in user_30d])

        self.assertEqual(sum(item["value"] for item in sales_7d), 128.0)
        self.assertEqual(sum(item["value"] for item in sales_30d), 128.0)
        self.assertEqual(sum(item["value"] for item in order_7d), 3)
        self.assertEqual(sum(item["value"] for item in order_30d), 3)
        self.assertEqual(sum(item["value"] for item in user_7d), 1)
        self.assertEqual(sum(item["value"] for item in user_30d), 1)

    def test_new_user_metrics_exclude_staff_and_superusers(self):
        seed_minimal_order_scenario()
        now = timezone.now()

        superuser = User.objects.create_superuser(
            username="analytics_admin",
            email="analytics_admin@example.com",
            password="test-password",
        )
        staff_user = User.objects.create_user(username="analytics_staff")
        User.objects.filter(pk=staff_user.pk).update(is_staff=True)
        User.objects.filter(pk__in=[superuser.pk, staff_user.pk]).update(
            date_joined=now - timedelta(days=1)
        )

        overview = build_overview_payload()
        dashboard = build_dashboard_payload()
        user_trend_7d = dashboard["sections"]["users"]["new_user_trend"]["7d"]
        user_trend_30d = dashboard["sections"]["users"]["new_user_trend"]["30d"]

        self.assertEqual(overview["metrics"]["new_users_count"], 1)
        self.assertEqual(sum(item["value"] for item in user_trend_7d), 1)
        self.assertEqual(sum(item["value"] for item in user_trend_30d), 1)

    def test_refund_alert_only_counts_pending_review_orders(self):
        seed_minimal_order_scenario()

        overview = build_overview_payload()
        refund_alert = next(
            alert for alert in overview["alerts"] if alert["title"] == "退款申请待审核"
        )

        self.assertIn("1 笔", refund_alert["description"])
        self.assertNotIn(
            "退款订单待处理",
            [alert["title"] for alert in overview["alerts"]],
        )

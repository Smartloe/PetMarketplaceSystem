from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from charts.services import build_dashboard_payload, build_overview_payload
from charts.tests.helpers import seed_minimal_order_scenario


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

from tempfile import TemporaryDirectory

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse


class SeedToDashboardSmokeTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="smoke_admin",
            password="AdminPass#2026",
            email="smoke@example.com",
        )

    def test_seeded_data_flows_from_command_to_api_and_admin_pages(self):
        with TemporaryDirectory() as tmp_media:
            with override_settings(MEDIA_ROOT=tmp_media, DEBUG=True):
                call_command("seed_demo_business_data")
                self.client.force_login(self.admin_user)

                overview_response = self.client.get("/api/charts/overview/")
                dashboard_response = self.client.get("/api/charts/dashboard/")
                admin_index_response = self.client.get(reverse("admin:index"))
                analytics_response = self.client.get(
                    reverse("admin:charts_soldmodel_changelist")
                )

        self.assertEqual(overview_response.status_code, 200)
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(admin_index_response, "经营概览")
        self.assertContains(analytics_response, "综合数据看板")
        self.assertGreater(overview_response.json()["metrics"]["order_count"], 0)
        self.assertGreater(
            dashboard_response.json()["sections"]["operations"]["order_count"],
            0,
        )

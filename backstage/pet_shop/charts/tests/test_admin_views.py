from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AnalyticsAdminViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            password="AdminPass#2026",
            email="admin@example.com",
        )
        self.client.force_login(self.admin_user)

    def test_sold_model_changelist_becomes_dashboard_entry(self):
        response = self.client.get(reverse("admin:charts_soldmodel_changelist"))
        dashboard_url = reverse("charts-dashboard")

        self.assertContains(response, "综合数据看板")
        self.assertContains(response, 'id="analytics-dashboard-root"')
        self.assertContains(response, f'data-dashboard-url="{dashboard_url}"')

    def test_admin_index_renders_overview_and_app_list(self):
        response = self.client.get(reverse("admin:index"))
        overview_url = reverse("charts-overview")

        self.assertContains(response, "经营概览")
        self.assertContains(response, f'data-overview-url="{overview_url}"')
        self.assertContains(response, reverse("admin:charts_soldmodel_changelist"))
        self.assertContains(response, "数据可视化")
        self.assertContains(response, 'id="recent-actions-module"')

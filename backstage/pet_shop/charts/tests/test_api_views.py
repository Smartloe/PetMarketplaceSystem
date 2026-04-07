from django.contrib.auth.models import User
from django.test import TestCase


class AnalyticsApiViewTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_superuser(
            username="api_admin",
            password="AdminPass#2026",
            email="api@example.com",
        )

    def test_overview_endpoint_redirects_anonymous_users(self):
        response = self.client.get("/api/charts/overview/")
        self.assertIn(response.status_code, {302, 403})

    def test_overview_endpoint_returns_metrics_payload_for_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get("/api/charts/overview/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("metrics", response.json())

    def test_dashboard_endpoint_returns_sectioned_payload_for_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get("/api/charts/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("sections", response.json())

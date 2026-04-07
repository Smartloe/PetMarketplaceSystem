import subprocess
from pathlib import Path

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
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
        self.assertContains(response, "admin_analytics/shared.js")
        self.assertNotContains(response, 'class="menu-content"')
        self.assertNotContains(response, "{&#x27;name&#x27;: &#x27;交易管理&#x27;")

    def test_admin_index_renders_overview_and_app_list(self):
        response = self.client.get(reverse("admin:index"))
        overview_url = reverse("charts-overview")

        self.assertContains(response, "经营概览")
        self.assertContains(response, f'data-overview-url="{overview_url}"')
        self.assertContains(response, 'body class="admin-overview-index"')
        self.assertContains(response, "admin_analytics/shared.js")
        self.assertContains(response, reverse("admin:charts_soldmodel_changelist"))
        self.assertContains(response, "数据可视化")
        self.assertContains(response, 'id="recent-actions-module"')
        self.assertNotContains(response, 'class="menu-content"')
        self.assertNotContains(response, "{&#x27;name&#x27;: &#x27;交易管理&#x27;")
        self.assertNotContains(response, " dashboard admin-overview-index")
        self.assertNotContains(response, "把后台首页做成“先扫一眼”的总控台")
        self.assertNotContains(response, "正在同步销售额与订单量变化。")
        self.assertNotContains(response, "继续使用 Django 管理后台默认应用列表与快捷入口。")


class AnalyticsStaticRegressionTests(SimpleTestCase):
    def _run_script(self, script_name):
        backend_root = Path(__file__).resolve().parents[2]
        script_path = backend_root / "charts" / "tests" / script_name
        result = subprocess.run(
            ["node", str(script_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"{script_name} exited with {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            ),
        )

    def test_dashboard_js_regression_script_passes(self):
        self._run_script("dashboard_js_regression_check.js")

    def test_overview_js_regression_script_passes(self):
        self._run_script("overview_js_regression_check.js")

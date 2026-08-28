from django.urls import path
from .views import dashboard_data, overview_data, overview_page

urlpatterns = [
    path("overview/", overview_data, name="charts-overview"),
    path("dashboard/", dashboard_data, name="charts-dashboard"),
    # 后台首页概览（HTML）。SIMPLEUI_HOME_PAGE 指向这里。
    path("overview/page/", overview_page, name="charts-overview-page"),
]

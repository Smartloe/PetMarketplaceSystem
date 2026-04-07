from django.urls import path
from .views import dashboard_data, overview_data

urlpatterns = [
    path("overview/", overview_data, name="charts-overview"),
    path("dashboard/", dashboard_data, name="charts-dashboard"),
]

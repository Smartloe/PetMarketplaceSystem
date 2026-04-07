from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from charts.services import build_dashboard_payload, build_overview_payload


@staff_member_required
def overview_data(request):
    return JsonResponse(build_overview_payload())


@staff_member_required
def dashboard_data(request):
    return JsonResponse(build_dashboard_payload())

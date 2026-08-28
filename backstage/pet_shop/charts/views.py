from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render

from charts.services import build_dashboard_payload, build_overview_payload


@staff_member_required
def overview_page(request):
    """
    首页经营概览，通过 SIMPLEUI_HOME_PAGE 挂进 SimpleUI 外壳的第一个标签页。

    模板里用到 app_list（管理入口）和 admin_log（最近操作），这两项平时由
    AdminSite.index 注入。这里是独立视图，所以显式补齐 —— each_context 提供
    站点标题等公共变量，app_list 则要单独取。
    """
    context = {
        **admin.site.each_context(request),
        "app_list": admin.site.get_app_list(request),
    }
    return render(request, "charts/overview_page.html", context)


@staff_member_required
def overview_data(request):
    return JsonResponse(build_overview_payload())


@staff_member_required
def dashboard_data(request):
    return JsonResponse(build_dashboard_payload())

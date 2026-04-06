from __future__ import annotations

from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.db.models import Avg, Case, CharField, Count, Q, Sum, Value, When
from django.db.models.functions import TruncDate
from django.utils import timezone

from charts.constants import (
    GMV_ALLOWED_REFUND_STATUSES,
    GMV_ORDER_STATUSES,
    LOW_STOCK_THRESHOLD,
    ORDER_COUNT_STATUSES,
    ORDER_STATUS_LABELS,
    PAY_METHOD_LABELS,
    PRICE_BANDS,
    REFUND_BUCKET_IN_PROGRESS,
    REFUND_BUCKET_RETURNED,
    TREND_WINDOWS,
)
from commodity.models import CommodityInfos
from customer_operation.models import UserComment
from trade.models import OrderGoods, OrderInfos

MONEY_ZERO = Decimal("0.00")
RATING_PRECISION = Decimal("0.01")
DASHBOARD_WINDOW_DAYS = TREND_WINDOWS[1]


def _today() -> date:
    return timezone.now().date()


def _window_start(days: int) -> date:
    return _today() - timedelta(days=days - 1)


def _window_bounds(days: int) -> tuple[date, date]:
    return _window_start(days), _today()


def _make_boundary_datetime(day: date) -> datetime:
    boundary = datetime.combine(day, time.min)
    if timezone.is_aware(timezone.now()) and timezone.is_naive(boundary):
        return timezone.make_aware(boundary, timezone.get_current_timezone())
    return boundary


def _window_datetime_bounds(days: int) -> tuple[datetime, datetime]:
    start_date, end_date = _window_bounds(days)
    return _make_boundary_datetime(start_date), _make_boundary_datetime(
        end_date + timedelta(days=1)
    )


def _format_money(value: Decimal | None) -> str:
    amount = value if value is not None else MONEY_ZERO
    return str(amount.quantize(MONEY_ZERO, rounding=ROUND_HALF_UP))


def _coerce_day(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _build_zero_filled_daily_series(days: int, rows_by_day: dict[date, int | Decimal]):
    start_date = _window_start(days)
    series = []
    for offset in range(days):
        day = start_date + timedelta(days=offset)
        raw_value = rows_by_day.get(day, 0)
        if isinstance(raw_value, Decimal):
            value = float(raw_value.quantize(MONEY_ZERO, rounding=ROUND_HALF_UP))
        else:
            value = raw_value or 0
        series.append({"date": day.strftime("%Y-%m-%d"), "value": value})
    return series


def _order_queryset(
    days: int | None = DASHBOARD_WINDOW_DAYS,
    included_statuses=None,
    refund_statuses=None,
):
    queryset = OrderInfos.objects.all()
    if days is not None:
        start_at, end_at = _window_datetime_bounds(days)
        queryset = queryset.filter(created_time__gte=start_at, created_time__lt=end_at)
    if included_statuses is not None:
        queryset = queryset.filter(order_status__in=included_statuses)
    if refund_statuses is not None:
        queryset = queryset.filter(refund_status__in=refund_statuses)
    return queryset


def _gmv_queryset(days: int):
    return _order_queryset(
        days=days,
        included_statuses=GMV_ORDER_STATUSES,
        refund_statuses=GMV_ALLOWED_REFUND_STATUSES,
    )


def _rows_to_day_map(rows):
    rows_by_day: dict[date, int | Decimal] = {}
    for row in rows:
        rows_by_day[_coerce_day(row["day"])] = row["value"] or 0
    return rows_by_day


def _calculate_gmv(days: int = 30) -> str:
    total = _gmv_queryset(days).aggregate(total=Sum("payable_price"))["total"] or MONEY_ZERO
    return _format_money(total)


def _calculate_order_count(days: int = 30, included_statuses=ORDER_COUNT_STATUSES) -> int:
    return _order_queryset(days=days, included_statuses=included_statuses).count()


def _calculate_new_users(days: int = 30) -> int:
    user_model = get_user_model()
    start_at, end_at = _window_datetime_bounds(days)
    return user_model.objects.filter(
        date_joined__gte=start_at,
        date_joined__lt=end_at,
    ).count()


def _calculate_average_order_value(
    days: int,
    order_statuses,
    refund_statuses,
) -> str:
    included_orders = _order_queryset(
        days=days,
        included_statuses=order_statuses,
        refund_statuses=refund_statuses,
    )
    aggregates = included_orders.aggregate(total=Sum("payable_price"), count=Count("id"))
    order_count = aggregates["count"] or 0
    if not order_count:
        return _format_money(MONEY_ZERO)
    total = aggregates["total"] or MONEY_ZERO
    return _format_money(total / Decimal(order_count))


def _build_daily_sales_trend(days: int):
    rows = (
        _gmv_queryset(days)
        .annotate(day=TruncDate("created_time"))
        .values("day")
        .annotate(value=Sum("payable_price"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(days, _rows_to_day_map(rows))


def _build_daily_order_trend(days: int):
    rows = (
        _order_queryset(days=days, included_statuses=ORDER_COUNT_STATUSES)
        .annotate(day=TruncDate("created_time"))
        .values("day")
        .annotate(value=Count("id"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(days, _rows_to_day_map(rows))


def _build_daily_user_trend(days: int):
    user_model = get_user_model()
    start_at, end_at = _window_datetime_bounds(days)
    rows = (
        user_model.objects.filter(date_joined__gte=start_at, date_joined__lt=end_at)
        .annotate(day=TruncDate("date_joined"))
        .values("day")
        .annotate(value=Count("id"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(days, _rows_to_day_map(rows))


def _build_category_share(days: int = DASHBOARD_WINDOW_DAYS):
    rows = (
        OrderGoods.objects.filter(
            order__order_status__in=ORDER_COUNT_STATUSES,
            order__in=_order_queryset(
                days=days,
                included_statuses=ORDER_COUNT_STATUSES,
            ),
        )
        .values("goods__types__title")
        .annotate(value=Sum("goods_num"))
        .order_by("-value", "goods__types__title")
    )
    return [
        {"name": row["goods__types__title"] or "未分类", "value": row["value"] or 0}
        for row in rows
    ]


def _build_hot_products(limit: int, days: int = DASHBOARD_WINDOW_DAYS):
    rows = (
        OrderGoods.objects.filter(
            order__order_status__in=ORDER_COUNT_STATUSES,
            order__in=_order_queryset(
                days=days,
                included_statuses=ORDER_COUNT_STATUSES,
            ),
        )
        .values("goods_id", "goods__sku_title", "goods__stock_quantity")
        .annotate(sold_quantity=Sum("goods_num"))
        .order_by("-sold_quantity", "goods_id")[:limit]
    )
    return [
        {
            "product_id": row["goods_id"],
            "title": row["goods__sku_title"],
            "sold_quantity": row["sold_quantity"] or 0,
            "stock_quantity": row["goods__stock_quantity"] or 0,
        }
        for row in rows
    ]


def _build_alerts():
    alerts = []
    low_stock_count = CommodityInfos.objects.filter(
        stock_quantity__lte=LOW_STOCK_THRESHOLD
    ).count()
    if low_stock_count:
        alerts.append(
            {
                "level": "warning",
                "title": "低库存商品提醒",
                "description": f"当前有 {low_stock_count} 个商品库存低于阈值，请尽快补货。",
                "target_url": "/admin/commodity/commodityinfos/",
            }
        )

    refund_review_count = OrderInfos.objects.filter(refund_status__in=(1, 2)).count()
    if refund_review_count:
        alerts.append(
            {
                "level": "warning",
                "title": "退款订单待处理",
                "description": f"当前有 {refund_review_count} 笔退款单需要跟进处理。",
                "target_url": "/admin/trade/orderinfos/",
            }
        )

    low_rating_count = UserComment.objects.filter(rating__lte=2).count()
    if low_rating_count:
        alerts.append(
            {
                "level": "warning",
                "title": "低评分评论提醒",
                "description": f"当前有 {low_rating_count} 条低评分评论，建议尽快排查。",
                "target_url": "/admin/customer_operation/usercomment/",
            }
        )

    return alerts


def _build_price_band_distribution():
    distribution = []
    for lower, upper, label in PRICE_BANDS:
        queryset = CommodityInfos.objects.filter(price__gte=Decimal(str(lower)))
        if upper is not None:
            queryset = queryset.filter(price__lte=Decimal(str(upper)))
        distribution.append({"name": label, "value": queryset.count()})
    return distribution


def _build_low_stock_products(limit: int = 10):
    products = CommodityInfos.objects.filter(
        stock_quantity__lte=LOW_STOCK_THRESHOLD
    ).order_by("stock_quantity", "id")[:limit]
    return [
        {
            "product_id": product.id,
            "title": product.sku_title,
            "stock_quantity": product.stock_quantity or 0,
            "sold_quantity": product.sold or 0,
        }
        for product in products
    ]


def _build_payment_method_distribution(days: int = DASHBOARD_WINDOW_DAYS):
    rows = (
        _order_queryset(days=days, included_statuses=ORDER_COUNT_STATUSES)
        .values("pay_method")
        .annotate(value=Count("id"))
    )
    counts = {row["pay_method"]: row["value"] for row in rows}
    return [
        {"name": name, "value": counts.get(code, 0)}
        for code, name in PAY_METHOD_LABELS.items()
    ]


def _build_order_status_distribution(days: int = DASHBOARD_WINDOW_DAYS):
    rows = _order_queryset(days=days).values("order_status").annotate(value=Count("id"))
    counts = {row["order_status"]: row["value"] for row in rows}
    return [
        {"name": name, "value": counts.get(code, 0)}
        for code, name in ORDER_STATUS_LABELS.items()
    ]


def _build_refund_distribution(days: int = DASHBOARD_WINDOW_DAYS):
    rows = (
        _order_queryset(days=days, included_statuses=ORDER_COUNT_STATUSES)
        .annotate(
            refund_bucket=Case(
                When(
                    Q(refund_status=2) | Q(order_status=5),
                    then=Value(REFUND_BUCKET_RETURNED),
                ),
                When(
                    Q(refund_status=1) | Q(order_status=4),
                    then=Value(REFUND_BUCKET_IN_PROGRESS),
                ),
                default=Value(None),
                output_field=CharField(),
            )
        )
        .exclude(refund_bucket__isnull=True)
        .values("refund_bucket")
        .annotate(value=Count("id"))
    )
    counts = {row["refund_bucket"]: row["value"] for row in rows}
    return [
        {
            "name": REFUND_BUCKET_IN_PROGRESS,
            "value": counts.get(REFUND_BUCKET_IN_PROGRESS, 0),
        },
        {
            "name": REFUND_BUCKET_RETURNED,
            "value": counts.get(REFUND_BUCKET_RETURNED, 0),
        },
    ]


def _build_province_distribution(days: int = DASHBOARD_WINDOW_DAYS):
    rows = (
        _order_queryset(days=days, included_statuses=ORDER_COUNT_STATUSES)
        .values("address__province")
        .annotate(value=Count("id"))
        .order_by("-value", "address__province")
    )
    return [
        {"name": row["address__province"] or "未知", "value": row["value"] or 0}
        for row in rows
    ]


def _build_rating_summary():
    aggregates = UserComment.objects.aggregate(
        average_rating=Avg("rating"),
        total_comments=Count("id"),
    )
    rating_counts = (
        UserComment.objects.values("rating")
        .annotate(value=Count("id"))
        .order_by("rating")
    )
    counts_by_rating = {row["rating"]: row["value"] for row in rating_counts}
    distribution = [
        {"name": f"{score}星", "value": counts_by_rating.get(score, 0)}
        for score in range(1, 6)
    ]

    average_rating = aggregates["average_rating"]
    formatted_rating = Decimal(str(average_rating or 0)).quantize(
        RATING_PRECISION,
        rounding=ROUND_HALF_UP,
    )
    return {
        "average_rating": str(formatted_rating),
        "total_comments": aggregates["total_comments"] or 0,
        "distribution": distribution,
    }


def build_overview_payload():
    days_short, days_long = TREND_WINDOWS
    return {
        "metrics": {
            "gmv": _calculate_gmv(days=days_long),
            "order_count": _calculate_order_count(
                days=days_long,
                included_statuses=ORDER_COUNT_STATUSES,
            ),
            "new_users_count": _calculate_new_users(days=days_long),
            "low_stock_count": CommodityInfos.objects.filter(
                stock_quantity__lte=LOW_STOCK_THRESHOLD
            ).count(),
        },
        "trends": {
            "sales": {
                "7d": _build_daily_sales_trend(days=days_short),
                "30d": _build_daily_sales_trend(days=days_long),
            },
            "orders": {
                "7d": _build_daily_order_trend(days=days_short),
                "30d": _build_daily_order_trend(days=days_long),
            },
        },
        "category_share": _build_category_share(days=days_long),
        "hot_products": _build_hot_products(limit=5, days=days_long),
        "alerts": _build_alerts(),
    }


def build_dashboard_payload():
    days_short, days_long = TREND_WINDOWS
    overview = build_overview_payload()
    return {
        "sections": {
            "operations": {
                "gmv": overview["metrics"]["gmv"],
                "order_count": overview["metrics"]["order_count"],
                "average_order_value": _calculate_average_order_value(
                    days=days_long,
                    order_statuses=GMV_ORDER_STATUSES,
                    refund_statuses=GMV_ALLOWED_REFUND_STATUSES,
                ),
                "payment_method_distribution": _build_payment_method_distribution(
                    days=days_long
                ),
            },
            "catalog": {
                "category_share": _build_category_share(days=days_long),
                "hot_products": _build_hot_products(limit=10, days=days_long),
                "price_band_distribution": _build_price_band_distribution(),
                "low_stock_products": _build_low_stock_products(),
            },
            "users": {
                "new_user_trend": {
                    "7d": _build_daily_user_trend(days=days_short),
                    "30d": _build_daily_user_trend(days=days_long),
                },
                "province_distribution": _build_province_distribution(days=days_long),
                "rating_summary": _build_rating_summary(),
            },
            "orders": {
                "status_distribution": _build_order_status_distribution(days=days_long),
                "refund_distribution": _build_refund_distribution(days=days_long),
                "sales_trend": {
                    "7d": _build_daily_sales_trend(days=days_short),
                    "30d": _build_daily_sales_trend(days=days_long),
                },
                "order_trend": {
                    "7d": _build_daily_order_trend(days=days_short),
                    "30d": _build_daily_order_trend(days=days_long),
                },
            },
        }
    }

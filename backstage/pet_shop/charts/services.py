from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass
class _AnalyticsTimeContext:
    now: datetime
    today: date
    window_bounds: dict[int, tuple[date, date]] = field(default_factory=dict)
    window_datetime_bounds: dict[int, tuple[datetime, datetime]] = field(
        default_factory=dict
    )


def _build_time_context(now: datetime | None = None) -> _AnalyticsTimeContext:
    current_now = now or timezone.now()
    return _AnalyticsTimeContext(now=current_now, today=current_now.date())


def _window_start(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
) -> date:
    context = time_context or _build_time_context()
    return context.today - timedelta(days=days - 1)


def _window_bounds(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
) -> tuple[date, date]:
    context = time_context or _build_time_context()
    if days not in context.window_bounds:
        context.window_bounds[days] = (_window_start(days, time_context=context), context.today)
    return context.window_bounds[days]


def _make_boundary_datetime(day: date, reference_now: datetime) -> datetime:
    boundary = datetime.combine(day, time.min)
    if timezone.is_aware(reference_now) and timezone.is_naive(boundary):
        return timezone.make_aware(boundary, timezone.get_current_timezone())
    return boundary


def _window_datetime_bounds(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
) -> tuple[datetime, datetime]:
    context = time_context or _build_time_context()
    if days not in context.window_datetime_bounds:
        start_date, end_date = _window_bounds(days, time_context=context)
        context.window_datetime_bounds[days] = (
            _make_boundary_datetime(start_date, reference_now=context.now),
            _make_boundary_datetime(
                end_date + timedelta(days=1),
                reference_now=context.now,
            ),
        )
    return context.window_datetime_bounds[days]


def _format_money(value: Decimal | None) -> str:
    amount = value if value is not None else MONEY_ZERO
    return str(amount.quantize(MONEY_ZERO, rounding=ROUND_HALF_UP))


def _coerce_day(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _build_zero_filled_daily_series(
    days: int,
    rows_by_day: dict[date, int | Decimal],
    time_context: _AnalyticsTimeContext | None = None,
):
    start_date = _window_start(days, time_context=time_context)
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
    time_context: _AnalyticsTimeContext | None = None,
):
    queryset = OrderInfos.objects.all()
    if days is not None:
        start_at, end_at = _window_datetime_bounds(days, time_context=time_context)
        queryset = queryset.filter(created_time__gte=start_at, created_time__lt=end_at)
    if included_statuses is not None:
        queryset = queryset.filter(order_status__in=included_statuses)
    if refund_statuses is not None:
        queryset = queryset.filter(refund_status__in=refund_statuses)
    return queryset


def _gmv_queryset(days: int, time_context: _AnalyticsTimeContext | None = None):
    return _order_queryset(
        days=days,
        included_statuses=GMV_ORDER_STATUSES,
        refund_statuses=GMV_ALLOWED_REFUND_STATUSES,
        time_context=time_context,
    )


def _rows_to_day_map(rows):
    rows_by_day: dict[date, int | Decimal] = {}
    for row in rows:
        rows_by_day[_coerce_day(row["day"])] = row["value"] or 0
    return rows_by_day


def _calculate_gmv(
    days: int = 30,
    time_context: _AnalyticsTimeContext | None = None,
) -> str:
    total = (
        _gmv_queryset(days, time_context=time_context).aggregate(total=Sum("payable_price"))[
            "total"
        ]
        or MONEY_ZERO
    )
    return _format_money(total)


def _calculate_order_count(
    days: int = 30,
    included_statuses=ORDER_COUNT_STATUSES,
    time_context: _AnalyticsTimeContext | None = None,
) -> int:
    return _order_queryset(
        days=days,
        included_statuses=included_statuses,
        time_context=time_context,
    ).count()


def _marketplace_users_queryset(user_model):
    return user_model.objects.filter(is_staff=False, is_superuser=False)


def _calculate_new_users(
    days: int = 30,
    time_context: _AnalyticsTimeContext | None = None,
) -> int:
    user_model = get_user_model()
    start_at, end_at = _window_datetime_bounds(days, time_context=time_context)
    return _marketplace_users_queryset(user_model).filter(
        date_joined__gte=start_at,
        date_joined__lt=end_at,
    ).count()


def _calculate_average_order_value(
    days: int,
    order_statuses,
    refund_statuses,
    time_context: _AnalyticsTimeContext | None = None,
) -> str:
    included_orders = _order_queryset(
        days=days,
        included_statuses=order_statuses,
        refund_statuses=refund_statuses,
        time_context=time_context,
    )
    aggregates = included_orders.aggregate(total=Sum("payable_price"), count=Count("id"))
    order_count = aggregates["count"] or 0
    if not order_count:
        return _format_money(MONEY_ZERO)
    total = aggregates["total"] or MONEY_ZERO
    return _format_money(total / Decimal(order_count))


def _build_daily_sales_trend(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
):
    rows = (
        _gmv_queryset(days, time_context=time_context)
        .annotate(day=TruncDate("created_time"))
        .values("day")
        .annotate(value=Sum("payable_price"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(
        days,
        _rows_to_day_map(rows),
        time_context=time_context,
    )


def _build_daily_order_trend(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
):
    rows = (
        _order_queryset(
            days=days,
            included_statuses=ORDER_COUNT_STATUSES,
            time_context=time_context,
        )
        .annotate(day=TruncDate("created_time"))
        .values("day")
        .annotate(value=Count("id"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(
        days,
        _rows_to_day_map(rows),
        time_context=time_context,
    )


def _build_daily_user_trend(
    days: int,
    time_context: _AnalyticsTimeContext | None = None,
):
    user_model = get_user_model()
    start_at, end_at = _window_datetime_bounds(days, time_context=time_context)
    rows = (
        _marketplace_users_queryset(user_model)
        .filter(date_joined__gte=start_at, date_joined__lt=end_at)
        .annotate(day=TruncDate("date_joined"))
        .values("day")
        .annotate(value=Count("id"))
        .order_by("day")
    )
    return _build_zero_filled_daily_series(
        days,
        _rows_to_day_map(rows),
        time_context=time_context,
    )


def _build_category_share(
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    start_at, end_at = _window_datetime_bounds(days, time_context=time_context)
    rows = (
        OrderGoods.objects.filter(
            order__created_time__gte=start_at,
            order__created_time__lt=end_at,
            order__order_status__in=GMV_ORDER_STATUSES,
            order__refund_status__in=GMV_ALLOWED_REFUND_STATUSES,
        )
        .values("goods__types__title")
        .annotate(value=Sum("goods_num"))
        .order_by("-value", "goods__types__title")
    )
    return [
        {"name": row["goods__types__title"] or "未分类", "value": row["value"] or 0}
        for row in rows
    ]


def _build_hot_products(
    limit: int,
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    start_at, end_at = _window_datetime_bounds(days, time_context=time_context)
    rows = (
        OrderGoods.objects.filter(
            order__created_time__gte=start_at,
            order__created_time__lt=end_at,
            order__order_status__in=GMV_ORDER_STATUSES,
            order__refund_status__in=GMV_ALLOWED_REFUND_STATUSES,
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


def _count_low_stock_products() -> int:
    return CommodityInfos.objects.filter(stock_quantity__lte=LOW_STOCK_THRESHOLD).count()


def _build_alerts(low_stock_count: int | None = None):
    alerts = []
    if low_stock_count is None:
        low_stock_count = _count_low_stock_products()
    if low_stock_count:
        alerts.append(
            {
                "level": "warning",
                "title": "低库存商品提醒",
                "description": f"当前有 {low_stock_count} 个商品库存低于阈值，请尽快补货。",
                "target_url": "/admin/commodity/commodityinfos/",
            }
        )

    refund_review_count = OrderInfos.objects.filter(refund_status=1).count()
    if refund_review_count:
        alerts.append(
            {
                "level": "warning",
                "title": "退款申请待审核",
                "description": f"当前有 {refund_review_count} 笔退款申请待审核，请及时处理。",
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


def _build_payment_method_distribution(
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    rows = (
        _order_queryset(
            days=days,
            included_statuses=ORDER_COUNT_STATUSES,
            time_context=time_context,
        )
        .values("pay_method")
        .annotate(value=Count("id"))
    )
    counts = {row["pay_method"]: row["value"] for row in rows}
    return [
        {"name": name, "value": counts.get(code, 0)}
        for code, name in PAY_METHOD_LABELS.items()
    ]


def _build_order_status_distribution(
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    rows = (
        _order_queryset(days=days, time_context=time_context)
        .values("order_status")
        .annotate(value=Count("id"))
    )
    counts = {row["order_status"]: row["value"] for row in rows}
    return [
        {"name": name, "value": counts.get(code, 0)}
        for code, name in ORDER_STATUS_LABELS.items()
    ]


def _build_refund_distribution(
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    """
    Task 2 refund contract:
    - "退款中" = `refund_status=1` OR `order_status=4`
    - "已退货" = `refund_status=2` OR `order_status=5`

    When an order satisfies both predicates (for example `order_status=4` with
    `refund_status=2`), map it to "已退货" to keep approved refunds out of the
    "退款中" bucket.
    """
    rows = (
        _order_queryset(
            days=days,
            included_statuses=ORDER_COUNT_STATUSES,
            time_context=time_context,
        )
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


def _build_province_distribution(
    days: int = DASHBOARD_WINDOW_DAYS,
    time_context: _AnalyticsTimeContext | None = None,
):
    rows = (
        _order_queryset(
            days=days,
            included_statuses=ORDER_COUNT_STATUSES,
            time_context=time_context,
        )
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


def _build_overview_core(
    *,
    days_short: int,
    days_long: int,
    hot_products_limit: int,
    include_alerts: bool,
    time_context: _AnalyticsTimeContext,
):
    low_stock_count = _count_low_stock_products()
    sales_trends = {
        "7d": _build_daily_sales_trend(days=days_short, time_context=time_context),
        "30d": _build_daily_sales_trend(days=days_long, time_context=time_context),
    }
    order_trends = {
        "7d": _build_daily_order_trend(days=days_short, time_context=time_context),
        "30d": _build_daily_order_trend(days=days_long, time_context=time_context),
    }
    payload = {
        "metrics": {
            "gmv": _calculate_gmv(days=days_long, time_context=time_context),
            "order_count": _calculate_order_count(
                days=days_long,
                included_statuses=ORDER_COUNT_STATUSES,
                time_context=time_context,
            ),
            "new_users_count": _calculate_new_users(
                days=days_long,
                time_context=time_context,
            ),
            "low_stock_count": low_stock_count,
        },
        "trends": {
            "sales": sales_trends,
            "orders": order_trends,
        },
        "category_share": _build_category_share(days=days_long, time_context=time_context),
        "hot_products": _build_hot_products(
            limit=hot_products_limit,
            days=days_long,
            time_context=time_context,
        ),
    }
    if include_alerts:
        payload["alerts"] = _build_alerts(low_stock_count=low_stock_count)
    return payload


def build_overview_payload():
    days_short, days_long = TREND_WINDOWS
    time_context = _build_time_context()
    return _build_overview_core(
        days_short=days_short,
        days_long=days_long,
        hot_products_limit=5,
        include_alerts=True,
        time_context=time_context,
    )


def build_dashboard_payload():
    days_short, days_long = TREND_WINDOWS
    time_context = _build_time_context()
    overview = _build_overview_core(
        days_short=days_short,
        days_long=days_long,
        hot_products_limit=10,
        include_alerts=False,
        time_context=time_context,
    )
    return {
        "sections": {
            "operations": {
                "gmv": overview["metrics"]["gmv"],
                "order_count": overview["metrics"]["order_count"],
                "average_order_value": _calculate_average_order_value(
                    days=days_long,
                    order_statuses=GMV_ORDER_STATUSES,
                    refund_statuses=GMV_ALLOWED_REFUND_STATUSES,
                    time_context=time_context,
                ),
                "payment_method_distribution": _build_payment_method_distribution(
                    days=days_long,
                    time_context=time_context,
                ),
            },
            "catalog": {
                "category_share": overview["category_share"],
                "hot_products": overview["hot_products"],
                "price_band_distribution": _build_price_band_distribution(),
                "low_stock_products": _build_low_stock_products(),
            },
            "users": {
                "new_user_trend": {
                    "7d": _build_daily_user_trend(
                        days=days_short,
                        time_context=time_context,
                    ),
                    "30d": _build_daily_user_trend(
                        days=days_long,
                        time_context=time_context,
                    ),
                },
                "province_distribution": _build_province_distribution(
                    days=days_long,
                    time_context=time_context,
                ),
                "rating_summary": _build_rating_summary(),
            },
            "orders": {
                "status_distribution": _build_order_status_distribution(
                    days=days_long,
                    time_context=time_context,
                ),
                "refund_distribution": _build_refund_distribution(
                    days=days_long,
                    time_context=time_context,
                ),
                "sales_trend": overview["trends"]["sales"],
                "order_trend": overview["trends"]["orders"],
            },
        }
    }

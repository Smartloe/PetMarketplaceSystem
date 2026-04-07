LOW_STOCK_THRESHOLD = 10
DEMO_USER_PREFIX = "demo_buyer"
DEMO_ORDER_PREFIX = "DEMO2026"
DEMO_CREATED_BY = "demo_seed"

TREND_WINDOWS = (7, 30)

GMV_ORDER_STATUSES = {1, 2, 3}
GMV_ALLOWED_REFUND_STATUSES = {0, 3}
ORDER_COUNT_STATUSES = {1, 2, 3, 4, 5}

PAY_METHOD_LABELS = {
    1: "微信",
    2: "支付宝",
    3: "银联",
}

ORDER_STATUS_LABELS = {
    0: "未支付",
    1: "已支付",
    2: "发货中",
    3: "已签收",
    4: "退货中",
    5: "已退货",
}

REFUND_STATUS_LABELS = {
    0: "无",
    1: "待审核",
    2: "已通过",
    3: "已拒绝",
}

REFUND_BUCKET_IN_PROGRESS = "退款中"
REFUND_BUCKET_RETURNED = "已退货"

PRICE_BANDS = (
    (0, 49.99, "0-49.99"),
    (50, 99.99, "50-99.99"),
    (100, 199.99, "100-199.99"),
    (200, None, "200及以上"),
)

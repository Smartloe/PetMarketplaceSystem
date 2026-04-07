(function () {
    function onReady(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback);
            return;
        }
        callback();
    }

    onReady(function () {
        var page = document.querySelector(".admin-analytics-page");
        if (!page) {
            return;
        }

        var dashboardUrl = page.getAttribute("data-dashboard-url");
        var statusElement = document.getElementById("dashboard-status");
        var root = document.getElementById("analytics-dashboard-root");
        var panels = {
            operations: document.getElementById("operations-panel"),
            catalog: document.getElementById("catalog-panel"),
            users: document.getElementById("users-panel"),
            orders: document.getElementById("orders-panel"),
        };
        var state = {
            payload: null,
            usersWindow: "30d",
            salesWindow: "30d",
            ordersWindow: "30d",
        };

        if (!dashboardUrl || !statusElement || !root) {
            return;
        }

        page.addEventListener("click", function (event) {
            var trigger = event.target.closest("[data-window-trigger]");
            if (trigger) {
                event.preventDefault();
                updateWindowState(trigger);
                return;
            }

            var action = event.target.closest("[data-dashboard-action='retry']");
            if (action) {
                event.preventDefault();
                fetchDashboard();
            }
        });

        fetchDashboard();

        function fetchDashboard() {
            setStatus(
                "loading",
                "正在同步综合数据看板",
                "正在拉取经营总览、商品分析、用户分析与订单分析，请稍候。"
            );
            root.setAttribute("data-state", "loading");

            window
                .fetch(dashboardUrl, {
                    credentials: "same-origin",
                    headers: {
                        Accept: "application/json",
                    },
                })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("HTTP " + response.status);
                    }
                    return response.json();
                })
                .then(function (payload) {
                    var sections = payload && payload.sections;
                    if (!sections || isDashboardEmpty(sections)) {
                        state.payload = payload || { sections: {} };
                        renderEmptyDashboard();
                        setStatus(
                            "empty",
                            "当前暂无可展示的经营数据",
                            "当订单、商品和评价陆续产生后，这里会自动汇总为完整的经营看板。"
                        );
                        root.setAttribute("data-state", "empty");
                        return;
                    }

                    state.payload = payload;
                    root.setAttribute("data-state", "ready");
                    renderDashboard(sections);
                    setStatus(
                        "ready",
                        "综合数据看板已更新",
                        "当前页面展示的是后台实时聚合数据，可用于快速查看近 30 天经营状态。"
                    );
                })
                .catch(function (error) {
                    root.setAttribute("data-state", "error");
                    renderErrorDashboard();
                    setStatus(
                        "error",
                        "获取经营数据失败",
                        "接口返回异常：" +
                            escapeHtml(error && error.message ? error.message : "未知错误") +
                            "。你可以稍后重试。",
                        true
                    );
                });
        }

        function renderDashboard(sections) {
            renderOperationsPanel(sections.operations || {});
            renderCatalogPanel(sections.catalog || {});
            renderUsersPanel(sections.users || {});
            renderOrdersPanel(sections.orders || {});
        }

        function renderEmptyDashboard() {
            renderPanel(
                panels.operations,
                "Operations",
                "经营总览",
                "交易指标与支付结构",
                renderEmptyBlock("暂无经营总览数据，待产生订单后这里会自动更新。")
            );
            renderPanel(
                panels.catalog,
                "Catalog",
                "商品分析",
                "分类表现、价格带与库存风险",
                renderEmptyBlock("暂无商品分析数据，可先关注商品分类、价格带与库存变化。")
            );
            renderPanel(
                panels.users,
                "Users",
                "用户分析",
                "新增趋势、地域分布与评价概况",
                renderEmptyBlock("暂无用户与评价数据，后续新增注册和评论后会自动聚合。")
            );
            renderPanel(
                panels.orders,
                "Orders",
                "订单分析",
                "状态分布、退款流向与趋势变化",
                renderEmptyBlock("暂无订单趋势数据，待交易发生后即可查看状态和走势。")
            );
        }

        function renderErrorDashboard() {
            var message = renderEmptyBlock("暂时无法渲染该模块，请稍后点击“重新获取”重试。");
            renderPanel(panels.operations, "Operations", "经营总览", "交易指标与支付结构", message);
            renderPanel(panels.catalog, "Catalog", "商品分析", "分类表现、价格带与库存风险", message);
            renderPanel(panels.users, "Users", "用户分析", "新增趋势、地域分布与评价概况", message);
            renderPanel(panels.orders, "Orders", "订单分析", "状态分布、退款流向与趋势变化", message);
        }

        function renderOperationsPanel(section) {
            var distribution = sortItems(section.payment_method_distribution);
            var leadPayment = distribution[0];
            var content =
                '<div class="module-grid module-grid--three">' +
                renderKpiCard("成交总额 GMV", formatCurrency(section.gmv), "近 30 天已完成支付订单") +
                renderKpiCard("订单总量", formatNumber(section.order_count), "包含当前统计口径内的有效订单") +
                renderKpiCard("客单价 AOV", formatCurrency(section.average_order_value), "成交金额 ÷ 有效订单数") +
                "</div>" +
                '<div class="module-grid module-grid--two">' +
                renderSubcard(
                    "支付方式结构",
                    "最近 30 天支付订单的渠道占比",
                    renderBarList(distribution, {
                        highlightFirst: true,
                        emptyText: "暂无支付方式数据。",
                    })
                ) +
                renderSubcard(
                    "经营观察",
                    leadPayment
                        ? "当前支付偏好与履约节奏"
                        : "等待更多支付数据",
                    '<ul class="note-list">' +
                        renderNoteItem("主力支付方式", leadPayment ? escapeHtml(leadPayment.name) : "暂无") +
                        renderNoteItem("支付渠道数", formatNumber(distribution.length || 0)) +
                        renderNoteItem("建议关注", "持续观察高峰日支付方式变化与订单转化") +
                    "</ul>"
                ) +
                "</div>";

            renderPanel(panels.operations, "Operations", "经营总览", "交易指标与支付结构", content);
        }

        function renderCatalogPanel(section) {
            var hotProducts = Array.isArray(section.hot_products) ? section.hot_products : [];
            var lowStockProducts = Array.isArray(section.low_stock_products)
                ? section.low_stock_products
                : [];

            var content =
                '<div class="module-grid module-grid--two">' +
                renderSubcard(
                    "分类销量占比",
                    "按已成交商品销量汇总",
                    renderBarList(sortItems(section.category_share), {
                        emptyText: "暂无分类销量数据。",
                    })
                ) +
                renderSubcard(
                    "价格带分布",
                    "当前在售商品的价格结构",
                    renderBarList(section.price_band_distribution, {
                        tone: "highlight",
                        emptyText: "暂无价格带数据。",
                    })
                ) +
                "</div>" +
                '<div class="module-grid module-grid--two">' +
                renderSubcard(
                    "热销商品清单",
                    "按近 30 天销量排序",
                    renderTable(
                        hotProducts,
                        [
                            { label: "商品", key: "title" },
                            { label: "销量", key: "sold_quantity", align: "right" },
                            { label: "库存", key: "stock_quantity", align: "right" },
                        ],
                        "暂无热销商品数据。"
                    )
                ) +
                renderSubcard(
                    "低库存预警",
                    "优先补货对象与近 30 天销量",
                    lowStockProducts.length
                        ? '<ul class="compact-list">' +
                          lowStockProducts
                              .map(function (item) {
                                  return (
                                      "<li><span>" +
                                      escapeHtml(item.title) +
                                      '</span><span><span class="pill pill--warning">库存 ' +
                                      formatNumber(item.stock_quantity) +
                                      "</span> <strong>近 30 天售出 " +
                                      formatNumber(item.sold_quantity) +
                                      "</strong></span></li>"
                                  );
                              })
                              .join("") +
                          "</ul>"
                        : renderEmptyBlock("暂无低库存商品，当前库存状态平稳。")
                ) +
                "</div>";

            renderPanel(panels.catalog, "Catalog", "商品分析", "分类表现、价格带与库存风险", content);
        }

        function renderUsersPanel(section) {
            var windowKey = state.usersWindow;
            var userTrend = section.new_user_trend || {};
            var trendSeries = Array.isArray(userTrend[windowKey]) ? userTrend[windowKey] : [];
            var latestUsers = trendSeries.length ? trendSeries[trendSeries.length - 1].value : 0;
            var ratingSummary = section.rating_summary || {};

            var content =
                '<div class="module-grid module-grid--two">' +
                renderSparklineCard(
                    "新增用户趋势",
                    "按注册时间汇总",
                    "users",
                    windowKey,
                    trendSeries,
                    "最近一天新增",
                    formatNumber(latestUsers)
                ) +
                renderSubcard(
                    "用户地域分布",
                    "基于订单地址省份聚合",
                    renderBarList(sortItems(section.province_distribution), {
                        emptyText: "暂无地域分布数据。",
                    })
                ) +
                "</div>" +
                renderSubcard(
                    "评价概况",
                    "评分均值与评论数量",
                    renderRatingSummary(ratingSummary)
                );

            renderPanel(panels.users, "Users", "用户分析", "新增趋势、地域分布与评价概况", content);
        }

        function renderOrdersPanel(section) {
            var salesSeries = Array.isArray((section.sales_trend || {})[state.salesWindow])
                ? section.sales_trend[state.salesWindow]
                : [];
            var orderSeries = Array.isArray((section.order_trend || {})[state.ordersWindow])
                ? section.order_trend[state.ordersWindow]
                : [];

            var latestSales = salesSeries.length ? salesSeries[salesSeries.length - 1].value : 0;
            var latestOrders = orderSeries.length ? orderSeries[orderSeries.length - 1].value : 0;

            var content =
                '<div class="module-grid module-grid--two">' +
                renderSubcard(
                    "订单状态分布",
                    "近 30 天订单流转概况",
                    renderBarList(sortItems(section.status_distribution), {
                        emptyText: "暂无订单状态数据。",
                    })
                ) +
                renderSubcard(
                    "退款流向",
                    "近 30 天退款申请与已退货统计",
                    renderBarList(section.refund_distribution, {
                        tone: "danger",
                        emptyText: "暂无退款数据。",
                    })
                ) +
                "</div>" +
                '<div class="module-grid module-grid--two">' +
                renderSparklineCard(
                    "销售额走势",
                    "按日统计近 7/30 天销售额",
                    "sales",
                    state.salesWindow,
                    salesSeries,
                    "最近一天销售额",
                    formatCurrency(latestSales)
                ) +
                renderSparklineCard(
                    "订单量走势",
                    "按日统计近 7/30 天订单数",
                    "orders",
                    state.ordersWindow,
                    orderSeries,
                    "最近一天订单量",
                    formatNumber(latestOrders)
                ) +
                "</div>";

            renderPanel(panels.orders, "Orders", "订单分析", "状态分布、退款流向与趋势变化", content);
        }

        function renderPanel(panel, eyebrow, title, caption, bodyHtml) {
            if (!panel) {
                return;
            }
            panel.innerHTML =
                '<div class="analytics-panel__header">' +
                "<div>" +
                '<p class="analytics-panel__eyebrow">' +
                escapeHtml(eyebrow) +
                "</p>" +
                "<h2>" +
                escapeHtml(title) +
                "</h2>" +
                "</div>" +
                '<p class="analytics-panel__caption">' +
                escapeHtml(caption) +
                "</p>" +
                "</div>" +
                bodyHtml;
        }

        function renderSubcard(title, caption, bodyHtml) {
            return (
                '<article class="subcard">' +
                '<div class="subcard__header">' +
                "<div>" +
                '<p class="subcard__eyebrow">Insight</p>' +
                "<h3>" +
                escapeHtml(title) +
                "</h3>" +
                "</div>" +
                '<p class="subcard__caption">' +
                escapeHtml(caption) +
                "</p>" +
                "</div>" +
                bodyHtml +
                "</article>"
            );
        }

        function renderKpiCard(label, value, footnote) {
            return (
                '<article class="kpi-card">' +
                '<span class="kpi-card__label">' +
                escapeHtml(label) +
                "</span>" +
                '<strong class="kpi-card__value">' +
                escapeHtml(value) +
                "</strong>" +
                '<p class="kpi-card__footnote">' +
                escapeHtml(footnote) +
                "</p>" +
                "</article>"
            );
        }

        function renderSparklineCard(title, caption, group, activeWindow, series, highlightLabel, highlightValue) {
            return (
                '<article class="subcard sparkline-card">' +
                '<div class="sparkline-card__header">' +
                "<div>" +
                '<p class="subcard__eyebrow">Trend</p>' +
                "<h3>" +
                escapeHtml(title) +
                "</h3>" +
                "</div>" +
                renderWindowSwitch(group, activeWindow) +
                "</div>" +
                '<p class="subcard__caption">' +
                escapeHtml(caption) +
                "</p>" +
                renderSparkline(series) +
                '<div class="sparkline-meta">' +
                "<span><span class=\"sparkline-meta__label\">" +
                escapeHtml(highlightLabel) +
                "</span><strong>" +
                escapeHtml(highlightValue) +
                "</strong></span>" +
                "<span><span class=\"sparkline-meta__label\">统计范围</span><strong>" +
                escapeHtml(activeWindow === "7d" ? "近 7 天" : "近 30 天") +
                "</strong></span>" +
                "</div>" +
                "</article>"
            );
        }

        function renderWindowSwitch(group, activeWindow) {
            return (
                '<div class="segmented-control" role="group" aria-label="切换时间窗口">' +
                renderWindowButton(group, "7d", activeWindow === "7d") +
                renderWindowButton(group, "30d", activeWindow === "30d") +
                "</div>"
            );
        }

        function renderWindowButton(group, value, active) {
            return (
                '<button type="button" data-window-trigger="' +
                escapeHtml(group) +
                '" data-window-value="' +
                escapeHtml(value) +
                '" class="' +
                (active ? "is-active" : "") +
                '">' +
                escapeHtml(value) +
                "</button>"
            );
        }

        function renderBarList(items, options) {
            var list = Array.isArray(items) ? items : [];
            var settings = options || {};
            if (!list.length) {
                return renderEmptyBlock(settings.emptyText || "暂无数据。");
            }

            var maxValue = list.reduce(function (current, item) {
                return Math.max(current, Number(item.value) || 0);
            }, 0);

            return (
                '<ul class="bar-list">' +
                list
                    .map(function (item, index) {
                        var toneClass = "";
                        if (settings.tone === "highlight") {
                            toneClass = " bar-fill--highlight";
                        } else if (settings.tone === "danger") {
                            toneClass = " bar-fill--danger";
                        } else if (settings.highlightFirst && index === 0) {
                            toneClass = " bar-fill--highlight";
                        }

                        return (
                            "<li>" +
                            '<div class="bar-list__meta"><span>' +
                            escapeHtml(item.name) +
                            '</span><span class="bar-list__value">' +
                            formatNumber(item.value) +
                            "</span></div>" +
                            '<div class="bar-track"><div class="bar-fill' +
                            toneClass +
                            '" style="width:' +
                            percentageWidth(item.value, maxValue) +
                            '%"></div></div>' +
                            "</li>"
                        );
                    })
                    .join("") +
                "</ul>"
            );
        }

        function renderTable(rows, columns, emptyText) {
            if (!Array.isArray(rows) || !rows.length) {
                return renderEmptyBlock(emptyText);
            }

            return (
                '<table class="data-table"><thead><tr>' +
                columns
                    .map(function (column) {
                        return (
                            '<th' +
                            (column.align ? ' data-align="' + column.align + '"' : "") +
                            ">" +
                            escapeHtml(column.label) +
                            "</th>"
                        );
                    })
                    .join("") +
                "</tr></thead><tbody>" +
                rows
                    .map(function (row) {
                        return (
                            "<tr>" +
                            columns
                                .map(function (column) {
                                    var value = row[column.key];
                                    var formattedValue =
                                        column.key === "title"
                                            ? escapeHtml(value)
                                            : formatNumber(value);
                                    return (
                                        '<td' +
                                        (column.align ? ' data-align="' + column.align + '"' : "") +
                                        ">" +
                                        formattedValue +
                                        "</td>"
                                    );
                                })
                                .join("") +
                            "</tr>"
                        );
                    })
                    .join("") +
                "</tbody></table>"
            );
        }

        function renderRatingSummary(summary) {
            var totalComments = summary && summary.total_comments ? summary.total_comments : 0;
            var averageRating = summary && summary.average_rating ? summary.average_rating : "0.00";
            var distribution = summary && Array.isArray(summary.distribution) ? summary.distribution : [];

            return (
                '<div class="rating-highlight">' +
                '<div class="rating-highlight__score">' +
                '<span class="card-label">平均评分</span>' +
                "<strong>" +
                escapeHtml(averageRating) +
                "</strong>" +
                '<p class="metric-inline">累计评论 <strong>' +
                formatNumber(totalComments) +
                "</strong> 条</p>" +
                "</div>" +
                "<div>" +
                renderBarList(distribution, {
                    highlightFirst: false,
                    emptyText: "暂无评论评分数据。",
                }) +
                "</div>" +
                "</div>"
            );
        }

        function renderSparkline(series) {
            if (!Array.isArray(series) || !series.length) {
                return renderEmptyBlock("暂无趋势数据。");
            }

            var values = series.map(function (item) {
                return Number(item.value) || 0;
            });
            var width = 520;
            var height = 180;
            var paddingX = 18;
            var paddingY = 20;
            var sparklineGeometry = buildSparklineGeometry(values, {
                width: width,
                height: height,
                paddingX: paddingX,
                paddingY: paddingY,
            });
            var points = sparklineGeometry.points;
            var areaPoints = sparklineGeometry.areaPoints;

            return (
                '<svg class="sparkline-chart" viewBox="0 0 ' +
                width +
                " " +
                height +
                '" role="img" aria-label="趋势图">' +
                '<polygon points="' +
                areaPoints +
                '" fill="rgba(47, 107, 99, 0.10)" stroke="none"></polygon>' +
                '<polyline points="' +
                points +
                '" fill="none" stroke="#2f6b63" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></polyline>' +
                values
                    .map(function (value, index) {
                        var point = points.split(" ")[index].split(",");
                        return (
                            '<circle cx="' +
                            point[0] +
                            '" cy="' +
                            point[1] +
                            '" r="4" fill="#ffffff" stroke="#2f6b63" stroke-width="2"></circle>'
                        );
                    })
                    .join("") +
                "</svg>" +
                '<div class="sparkline-axis"><span>' +
                escapeHtml(getSeriesLabel(series[0])) +
                "</span><span>" +
                escapeHtml(getSeriesLabel(series[series.length - 1])) +
                "</span></div>"
            );
        }

        function renderNoteItem(label, value) {
            return "<li><span>" + escapeHtml(label) + "</span><strong>" + escapeHtml(value) + "</strong></li>";
        }

        function renderEmptyBlock(message) {
            return (
                '<div class="empty-block">' +
                "<p>" +
                escapeHtml(message) +
                "</p>" +
                "</div>"
            );
        }

        function setStatus(kind, title, description, showRetry) {
            var className = "analytics-status";
            if (kind === "loading") {
                className += " analytics-status--loading";
            } else if (kind === "error") {
                className += " analytics-status--error";
            } else if (kind === "empty") {
                className += " analytics-status--empty";
            }

            statusElement.className = className;
            statusElement.innerHTML =
                '<div class="analytics-status__copy">' +
                "<strong>" +
                escapeHtml(title) +
                "</strong>" +
                "<p>" +
                description +
                "</p>" +
                "</div>" +
                (showRetry
                    ? '<button type="button" class="analytics-action" data-dashboard-action="retry">重新获取</button>'
                    : "");
        }

        function updateWindowState(trigger) {
            if (!state.payload || !state.payload.sections) {
                return;
            }

            var target = trigger.getAttribute("data-window-trigger");
            var value = trigger.getAttribute("data-window-value");
            if (!value || (value !== "7d" && value !== "30d")) {
                return;
            }

            if (target === "users") {
                state.usersWindow = value;
                renderUsersPanel(state.payload.sections.users || {});
            } else if (target === "sales") {
                state.salesWindow = value;
                renderOrdersPanel(state.payload.sections.orders || {});
            } else if (target === "orders") {
                state.ordersWindow = value;
                renderOrdersPanel(state.payload.sections.orders || {});
            }
        }

        function isDashboardEmpty(sections) {
            return !hasUsefulContent(sections.operations) &&
                !hasUsefulContent(sections.catalog) &&
                !hasUsefulContent(sections.users) &&
                !hasUsefulContent(sections.orders);
        }

        function hasUsefulContent(value) {
            if (Array.isArray(value)) {
                return value.some(function (item) {
                    return hasUsefulContent(item);
                });
            }

            if (!value || typeof value !== "object") {
                return isMeaningfulScalar(value);
            }

            if (isSeriesPoint(value) || isNamedMetric(value)) {
                return isMeaningfulScalar(value.value);
            }

            return Object.keys(value).some(function (key) {
                return hasUsefulContent(value[key]);
            });
        }

        function isSeriesPoint(value) {
            return hasOwn(value, "date") &&
                hasOwn(value, "value") &&
                Object.keys(value).length === 2;
        }

        function isNamedMetric(value) {
            return hasOwn(value, "name") &&
                hasOwn(value, "value") &&
                Object.keys(value).length === 2;
        }

        function buildSparklineGeometry(values, options) {
            var settings = options || {};
            var width = settings.width || 520;
            var height = settings.height || 180;
            var paddingX = settings.paddingX || 18;
            var paddingY = settings.paddingY || 20;
            var baselineY = height - paddingY;
            var chartWidth = width - paddingX * 2;
            var chartHeight = height - paddingY * 2;
            var denominator = values.length > 1 ? values.length - 1 : 1;
            var maxValue = Math.max.apply(null, values);
            var minValue = Math.min.apply(null, values);
            var hasFlatSeries = maxValue === minValue;
            var flatLineY = maxValue > 0
                ? baselineY - chartHeight / 2
                : baselineY;

            var pointList = values.map(function (value, index) {
                var x = paddingX + (chartWidth * index) / denominator;
                var y = hasFlatSeries
                    ? flatLineY
                    : baselineY - ((value - minValue) / (maxValue - minValue)) * chartHeight;
                return {
                    x: x.toFixed(2),
                    y: y.toFixed(2),
                };
            });

            return {
                points: pointList
                    .map(function (point) {
                        return point.x + "," + point.y;
                    })
                    .join(" "),
                areaPoints:
                    paddingX +
                    "," +
                    baselineY +
                    " " +
                    pointList
                        .map(function (point) {
                            return point.x + "," + point.y;
                        })
                        .join(" ") +
                    " " +
                    (paddingX + chartWidth) +
                    "," +
                    baselineY,
            };
        }

        function isMeaningfulScalar(value) {
            if (value === null || value === undefined || value === "") {
                return false;
            }
            if (typeof value === "number") {
                return value !== 0;
            }
            if (typeof value === "string") {
                var numeric = Number(value);
                return Number.isNaN(numeric) ? true : numeric !== 0;
            }
            return Boolean(value);
        }

        function sortItems(items) {
            if (!Array.isArray(items)) {
                return [];
            }
            return items.slice().sort(function (left, right) {
                return (Number(right.value) || 0) - (Number(left.value) || 0);
            });
        }

        function percentageWidth(value, maxValue) {
            var numericValue = Number(value) || 0;
            if (!maxValue || !numericValue) {
                return 0;
            }
            return Math.max(6, Math.round((numericValue / maxValue) * 100));
        }

        function formatCurrency(value) {
            var amount = Number(value) || 0;
            return "¥" + amount.toLocaleString("zh-CN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
        }

        function formatNumber(value) {
            return (Number(value) || 0).toLocaleString("zh-CN");
        }

        function getSeriesLabel(item) {
            if (!item || !item.date) {
                return "暂无";
            }
            return String(item.date).slice(5).replace("-", ".");
        }

        function hasOwn(value, key) {
            return Object.prototype.hasOwnProperty.call(value, key);
        }

        function escapeHtml(value) {
            return String(value === null || value === undefined ? "" : value)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\"/g, "&quot;")
                .replace(/'/g, "&#39;");
        }
    });
})();

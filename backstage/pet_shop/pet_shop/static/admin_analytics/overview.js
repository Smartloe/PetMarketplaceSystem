(function () {
    function onReady(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback);
            return;
        }
        callback();
    }

    onReady(function () {
        var page = document.querySelector(".admin-overview");
        if (!page) {
            return;
        }

        var overviewUrl = page.getAttribute("data-overview-url");
        var statusElement = document.getElementById("overview-status");
        var root = document.getElementById("admin-overview-root");
        var panels = {
            metrics: document.getElementById("overview-metrics"),
            trend: document.getElementById("overview-trend-chart"),
            share: document.getElementById("overview-share-chart"),
            hotProducts: document.getElementById("overview-hot-products"),
            alerts: document.getElementById("overview-alerts"),
        };
        var chartRegistry = {
            trend: null,
            share: null,
        };
        var state = {
            payload: null,
            trendMetric: "sales",
            trendWindow: "30d",
        };

        if (!overviewUrl || !statusElement || !root) {
            return;
        }

        page.addEventListener("click", function (event) {
            var metricTrigger = event.target.closest("[data-overview-metric]");
            if (metricTrigger) {
                event.preventDefault();
                state.trendMetric = metricTrigger.getAttribute("data-overview-metric") || "sales";
                renderTrendPanel();
                return;
            }

            var windowTrigger = event.target.closest("[data-overview-window]");
            if (windowTrigger) {
                event.preventDefault();
                state.trendWindow = windowTrigger.getAttribute("data-overview-window") || "30d";
                renderTrendPanel();
                return;
            }

            var retryTrigger = event.target.closest("[data-overview-action='retry']");
            if (retryTrigger) {
                event.preventDefault();
                fetchOverview();
            }
        });

        if (window.addEventListener) {
            window.addEventListener("resize", debounce(function () {
                resizeCharts();
            }, 120));
        }

        fetchOverview();

        function fetchOverview() {
            state.payload = null;
            root.setAttribute("data-state", "loading");
            renderLoadingOverview();
            setStatus(
                "loading",
                "正在同步首页经营概览",
                "正在拉取近 30 天经营指标、走势变化与待处理提醒，请稍候。"
            );

            window
                .fetch(overviewUrl, {
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
                    if (!payload || isOverviewEmpty(payload)) {
                        root.setAttribute("data-state", "empty");
                        renderEmptyOverview();
                        setStatus(
                            "empty",
                            "当前暂无可展示的首页概览",
                            "当订单、商品、用户与评论逐步产生后，这里会自动汇总成首页经营概览。"
                        );
                        return;
                    }

                    state.payload = payload;
                    root.setAttribute("data-state", "ready");
                    renderOverview(payload);
                    setStatus(
                        "ready",
                        "首页经营概览已更新",
                        "核心指标、走势、热销商品与待处理提醒已经同步，可继续进入完整分析页查看细分模块。"
                    );
                })
                .catch(function (error) {
                    root.setAttribute("data-state", "error");
                    renderErrorOverview();
                    setStatus(
                        "error",
                        "获取首页经营概览失败",
                        "接口返回异常：" +
                            escapeHtml(error && error.message ? error.message : "未知错误") +
                            "。你可以稍后重试。",
                        true
                    );
                });
        }

        function renderOverview(payload) {
            renderMetrics(payload.metrics || {});
            renderTrendPanel();
            renderSharePanel(payload.category_share || []);
            renderHotProductsPanel(payload.hot_products || []);
            renderAlertsPanel(payload.alerts || []);
        }

        function renderLoadingOverview() {
            disposeCharts();
            panels.metrics.innerHTML =
                renderKpiCard("GMV", "--", "正在同步近 30 天成交额") +
                renderKpiCard("订单数", "--", "正在同步有效订单总量") +
                renderKpiCard("新增用户", "--", "正在同步近 30 天新增注册") +
                renderKpiCard("低库存提醒", "--", "正在同步待补货商品数量");
            panels.trend.innerHTML = renderPanel(
                "Trend",
                "近 7 / 30 天走势",
                "销售额与订单量的首页快照",
                renderEmptyBlock("正在连接经营走势数据。")
            );
            panels.share.innerHTML = renderPanel(
                "Category Share",
                "分类销量占比",
                "按近 30 天销量聚合类目热度",
                renderEmptyBlock("正在连接分类占比数据。")
            );
            panels.hotProducts.innerHTML = renderPanel(
                "Hot Products",
                "热销商品",
                "按近 30 天销量筛选最值得关注的商品",
                renderEmptyBlock("正在连接热销商品数据。")
            );
            panels.alerts.innerHTML = renderPanel(
                "Alerts",
                "待处理提醒",
                "低库存、退款与低评分评论预警",
                renderEmptyBlock("正在连接待处理提醒数据。")
            );
        }

        function renderEmptyOverview() {
            disposeCharts();
            panels.metrics.innerHTML =
                renderKpiCard("GMV", formatCurrency(0), "当前统计周期内暂无成交额") +
                renderKpiCard("订单数", formatNumber(0), "当前统计周期内暂无有效订单") +
                renderKpiCard("新增用户", formatNumber(0), "当前统计周期内暂无新增注册") +
                renderKpiCard("低库存提醒", formatNumber(0), "当前没有待补货商品");
            panels.trend.innerHTML = renderPanel(
                "Trend",
                "近 7 / 30 天走势",
                "销售额与订单量的首页快照",
                renderEmptyBlock("暂无趋势数据，待订单产生后即可在首页查看走势变化。")
            );
            panels.share.innerHTML = renderPanel(
                "Category Share",
                "分类销量占比",
                "按近 30 天销量聚合类目热度",
                renderEmptyBlock("暂无分类销量数据，可先通过后台上架商品并完成订单。")
            );
            panels.hotProducts.innerHTML = renderPanel(
                "Hot Products",
                "热销商品",
                "按近 30 天销量筛选最值得关注的商品",
                renderEmptyBlock("暂无热销商品数据，等首批成交产生后会自动更新。")
            );
            panels.alerts.innerHTML = renderPanel(
                "Alerts",
                "待处理提醒",
                "低库存、退款与低评分评论预警",
                renderEmptyBlock("当前暂无库存、退款或口碑异常提醒。")
            );
        }

        function renderErrorOverview() {
            disposeCharts();
            panels.metrics.innerHTML =
                renderKpiCard("GMV", "--", "概览接口暂时不可用") +
                renderKpiCard("订单数", "--", "概览接口暂时不可用") +
                renderKpiCard("新增用户", "--", "概览接口暂时不可用") +
                renderKpiCard("低库存提醒", "--", "概览接口暂时不可用");
            panels.trend.innerHTML = renderPanel(
                "Trend",
                "近 7 / 30 天走势",
                "销售额与订单量的首页快照",
                renderEmptyBlock("暂时无法渲染趋势图，请稍后点击“重新获取”。")
            );
            panels.share.innerHTML = renderPanel(
                "Category Share",
                "分类销量占比",
                "按近 30 天销量聚合类目热度",
                renderEmptyBlock("暂时无法渲染分类占比，请稍后点击“重新获取”。")
            );
            panels.hotProducts.innerHTML = renderPanel(
                "Hot Products",
                "热销商品",
                "按近 30 天销量筛选最值得关注的商品",
                renderEmptyBlock("暂时无法渲染热销商品，请稍后点击“重新获取”。")
            );
            panels.alerts.innerHTML = renderPanel(
                "Alerts",
                "待处理提醒",
                "低库存、退款与低评分评论预警",
                renderEmptyBlock("暂时无法渲染提醒列表，请稍后点击“重新获取”。")
            );
        }

        function renderMetrics(metrics) {
            panels.metrics.innerHTML =
                renderKpiCard("GMV", formatCurrency(metrics.gmv), "近 30 天成交总额") +
                renderKpiCard("订单数", formatNumber(metrics.order_count), "近 30 天有效订单总量") +
                renderKpiCard("新增用户", formatNumber(metrics.new_users_count), "近 30 天新增注册用户") +
                renderKpiCard("低库存提醒", formatNumber(metrics.low_stock_count), "库存低于阈值的商品数量");
        }

        function renderTrendPanel() {
            var payload = state.payload || {};
            var trends = payload.trends || {};
            var group = trends[state.trendMetric] || {};
            var series = Array.isArray(group[state.trendWindow]) ? group[state.trendWindow] : [];
            var metricLabel = state.trendMetric === "orders" ? "订单量" : "销售额";
            var latestValue = series.length ? series[series.length - 1].value : 0;
            var secondaryValue =
                state.trendMetric === "orders"
                    ? formatNumber(latestValue)
                    : formatCurrency(latestValue);

            panels.trend.innerHTML = renderPanel(
                "Trend",
                "近 7 / 30 天走势",
                "用首页视角快速判断销售额与订单量的节奏变化",
                !series.length
                    ? renderEmptyBlock("暂无趋势数据。")
                    : '<div class="overview-toolbar">' +
                          '<div class="overview-toolbar__group">' +
                          '<span class="card-label">指标切换</span>' +
                          renderToggleGroup(
                              "切换趋势指标",
                              [
                                  { value: "sales", label: "销售额" },
                                  { value: "orders", label: "订单量" },
                              ],
                              state.trendMetric,
                              "data-overview-metric"
                          ) +
                          "</div>" +
                          '<div class="overview-toolbar__group">' +
                          '<span class="card-label">时间窗口</span>' +
                          renderToggleGroup(
                              "切换趋势时间窗口",
                              [
                                  { value: "7d", label: "近 7 天" },
                                  { value: "30d", label: "近 30 天" },
                              ],
                              state.trendWindow,
                              "data-overview-window"
                          ) +
                          "</div>" +
                      "</div>" +
                      '<div class="overview-chart-shell">' +
                          '<div id="overview-trend-canvas" class="overview-chart-canvas" role="img" aria-label="首页经营趋势图"></div>' +
                          '<div class="sparkline-meta">' +
                              "<span><span class=\"sparkline-meta__label\">当前指标</span><strong>" +
                              escapeHtml(metricLabel) +
                              "</strong></span>" +
                              "<span><span class=\"sparkline-meta__label\">最近一天</span><strong>" +
                              escapeHtml(secondaryValue) +
                              "</strong></span>" +
                          "</div>" +
                      "</div>"
            );

            if (!series.length) {
                disposeChart("trend");
                return;
            }

            if (!renderTrendEChart(series, state.trendMetric)) {
                renderTrendFallback(series);
            }
        }

        function renderSharePanel(items) {
            var sortedItems = sortItems(items);
            var leadCategory = sortedItems[0];
            var totalVolume = sortedItems.reduce(function (sum, item) {
                return sum + (Number(item.value) || 0);
            }, 0);

            panels.share.innerHTML = renderPanel(
                "Category Share",
                "分类销量占比",
                "按近 30 天销量聚合类目热度",
                !sortedItems.length
                    ? renderEmptyBlock("暂无分类销量数据。")
                    : '<div class="overview-split">' +
                          '<div id="overview-share-canvas" class="overview-chart-canvas overview-chart-canvas--compact" role="img" aria-label="分类销量占比图"></div>' +
                          "<div>" +
                              renderBarList(sortedItems, {
                                  highlightFirst: true,
                                  emptyText: "暂无分类销量数据。",
                              }) +
                              '<ul class="note-list">' +
                                  renderNoteItem("主力分类", leadCategory ? leadCategory.name : "暂无") +
                                  renderNoteItem("覆盖分类", formatNumber(sortedItems.length)) +
                                  renderNoteItem("累计销量", formatNumber(totalVolume)) +
                              "</ul>" +
                          "</div>" +
                      "</div>"
            );

            if (!sortedItems.length) {
                disposeChart("share");
                return;
            }

            if (!renderShareEChart(sortedItems)) {
                renderShareFallback(sortedItems);
            }
        }

        function renderHotProductsPanel(products) {
            var rows = Array.isArray(products) ? products : [];

            panels.hotProducts.innerHTML = renderPanel(
                "Hot Products",
                "热销商品",
                "按近 30 天销量筛选最值得关注的商品",
                !rows.length
                    ? renderEmptyBlock("暂无热销商品数据。")
                    : '<ol class="overview-rank-list">' +
                          rows
                              .map(function (item, index) {
                                  return (
                                      "<li>" +
                                      '<span class="overview-rank-list__index">' +
                                      escapeHtml(String(index + 1).padStart(2, "0")) +
                                      "</span>" +
                                      '<div class="overview-rank-list__copy">' +
                                      "<strong>" +
                                      escapeHtml(item.title) +
                                      "</strong>" +
                                      "<span>库存 " +
                                      formatNumber(item.stock_quantity) +
                                      " 件</span>" +
                                      "</div>" +
                                      '<div class="overview-rank-list__meta">' +
                                      '<span class="pill">售出 ' +
                                      formatNumber(item.sold_quantity) +
                                      "</span>" +
                                      "</div>" +
                                      "</li>"
                                  );
                              })
                              .join("") +
                      "</ol>"
            );
        }

        function renderAlertsPanel(alerts) {
            var rows = Array.isArray(alerts) ? alerts : [];

            panels.alerts.innerHTML = renderPanel(
                "Alerts",
                "待处理提醒",
                "低库存、退款与低评分评论预警",
                !rows.length
                    ? renderEmptyBlock("当前暂无库存、退款或口碑异常提醒。")
                    : '<div class="overview-alert-list">' +
                          rows
                              .map(function (item) {
                                  var levelClass = item.level === "danger" ? " pill--danger" : " pill--warning";
                                  return (
                                      '<article class="overview-alert">' +
                                      '<div class="overview-alert__title">' +
                                      "<strong>" +
                                      escapeHtml(item.title) +
                                      "</strong>" +
                                      '<span class="pill' +
                                      levelClass +
                                      '">' +
                                      escapeHtml(item.level === "danger" ? "紧急" : "预警") +
                                      "</span>" +
                                      "</div>" +
                                      '<p class="overview-alert__description">' +
                                      escapeHtml(item.description) +
                                      "</p>" +
                                      (item.target_url
                                          ? '<a class="overview-link" href="' +
                                                escapeHtml(item.target_url) +
                                                '">前往处理</a>'
                                          : "") +
                                      "</article>"
                                  );
                              })
                              .join("") +
                      "</div>"
            );
        }

        function renderTrendEChart(series, metric) {
            var chartElement = document.getElementById("overview-trend-canvas");
            if (!chartElement || !window.echarts || typeof window.echarts.init !== "function") {
                return false;
            }

            disposeChart("trend");
            chartRegistry.trend = window.echarts.init(chartElement, null, {
                renderer: "svg",
            });
            chartRegistry.trend.setOption({
                animationDuration: 400,
                color: ["#2f6b63"],
                tooltip: {
                    trigger: "axis",
                    backgroundColor: "#173047",
                    borderWidth: 0,
                    textStyle: {
                        color: "#f8fafc",
                    },
                    formatter: function (params) {
                        var point = params && params[0];
                        if (!point) {
                            return "";
                        }
                        return (
                            escapeHtml(point.axisValueLabel) +
                            "<br>" +
                            escapeHtml(metric === "orders" ? formatNumber(point.data) : formatCurrency(point.data))
                        );
                    },
                },
                grid: {
                    top: 28,
                    right: 20,
                    bottom: 30,
                    left: 56,
                },
                xAxis: {
                    type: "category",
                    boundaryGap: false,
                    data: series.map(function (item) {
                        return getSeriesLabel(item);
                    }),
                    axisLine: {
                        lineStyle: {
                            color: "#d7e0ea",
                        },
                    },
                    axisLabel: {
                        color: "#5f7285",
                    },
                    axisTick: {
                        show: false,
                    },
                },
                yAxis: {
                    type: "value",
                    axisLabel: {
                        color: "#5f7285",
                        formatter: function (value) {
                            if (metric === "orders") {
                                return formatCompactNumber(value);
                            }
                            return "¥" + formatCompactNumber(value);
                        },
                    },
                    splitLine: {
                        lineStyle: {
                            color: "rgba(95, 114, 133, 0.16)",
                        },
                    },
                },
                series: [
                    {
                        type: "line",
                        smooth: true,
                        showSymbol: false,
                        symbolSize: 8,
                        lineStyle: {
                            width: 3,
                        },
                        areaStyle: {
                            color: "rgba(47, 107, 99, 0.12)",
                        },
                        data: series.map(function (item) {
                            return Number(item.value) || 0;
                        }),
                    },
                ],
            });
            return true;
        }

        function renderTrendFallback(series) {
            var chartElement = document.getElementById("overview-trend-canvas");
            if (!chartElement) {
                return;
            }
            chartElement.innerHTML = renderSparkline(series);
        }

        function renderShareEChart(items) {
            var chartElement = document.getElementById("overview-share-canvas");
            if (!chartElement || !window.echarts || typeof window.echarts.init !== "function") {
                return false;
            }

            disposeChart("share");
            chartRegistry.share = window.echarts.init(chartElement, null, {
                renderer: "svg",
            });
            chartRegistry.share.setOption({
                animationDuration: 400,
                color: ["#2f6b63", "#5f938b", "#d98324", "#87b6d9", "#c96e5b", "#8a9db0"],
                tooltip: {
                    trigger: "item",
                    backgroundColor: "#173047",
                    borderWidth: 0,
                    textStyle: {
                        color: "#f8fafc",
                    },
                    formatter: function (params) {
                        return escapeHtml(params.name + " · " + formatNumber(params.value));
                    },
                },
                series: [
                    {
                        type: "pie",
                        radius: ["48%", "74%"],
                        center: ["50%", "46%"],
                        avoidLabelOverlap: true,
                        label: {
                            show: false,
                        },
                        labelLine: {
                            show: false,
                        },
                        itemStyle: {
                            borderColor: "#ffffff",
                            borderWidth: 3,
                        },
                        data: items.map(function (item) {
                            return {
                                name: item.name,
                                value: Number(item.value) || 0,
                            };
                        }),
                    },
                ],
            });
            return true;
        }

        function renderShareFallback(items) {
            var chartElement = document.getElementById("overview-share-canvas");
            if (!chartElement) {
                return;
            }
            var total = items.reduce(function (sum, item) {
                return sum + (Number(item.value) || 0);
            }, 0);
            chartElement.innerHTML =
                '<div class="overview-share-fallback">' +
                    '<div class="overview-share-strip" aria-hidden="true">' +
                        items
                            .map(function (item, index) {
                                return (
                                    '<span class="overview-share-strip__segment overview-share-strip__segment--' +
                                    (index % 6) +
                                    '" style="width:' +
                                    sharePercentage(item.value, total) +
                                    '%"></span>'
                                );
                            })
                            .join("") +
                    "</div>" +
                    '<ul class="tag-list overview-share-tags">' +
                        items
                            .slice(0, 4)
                            .map(function (item, index) {
                                return (
                                    '<li><span class="overview-share-dot overview-share-dot--' +
                                    (index % 6) +
                                    '"></span><span>' +
                                    escapeHtml(item.name) +
                                    '</span><strong>' +
                                    formatNumber(item.value) +
                                    "</strong></li>"
                                );
                            })
                            .join("") +
                    "</ul>" +
                "</div>";
        }

        function renderPanel(eyebrow, title, caption, bodyHtml) {
            return (
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
                bodyHtml
            );
        }

        function renderToggleGroup(label, options, activeValue, attributeName) {
            return (
                '<div class="segmented-control" role="group" aria-label="' +
                escapeHtml(label) +
                '">' +
                options
                    .map(function (item) {
                        return (
                            '<button type="button" ' +
                            attributeName +
                            '="' +
                            escapeHtml(item.value) +
                            '" class="' +
                            (item.value === activeValue ? "is-active" : "") +
                            '">' +
                            escapeHtml(item.label) +
                            "</button>"
                        );
                    })
                    .join("") +
                "</div>"
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

        function renderEmptyBlock(message) {
            return (
                '<div class="empty-block">' +
                    "<p>" +
                    escapeHtml(message) +
                    "</p>" +
                "</div>"
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
                        var toneClass = settings.highlightFirst && index === 0 ? " bar-fill--highlight" : "";
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

        function renderNoteItem(label, value) {
            return (
                "<li><span>" +
                escapeHtml(label) +
                "</span><strong>" +
                escapeHtml(value) +
                "</strong></li>"
            );
        }

        function renderSparkline(series) {
            if (!Array.isArray(series) || !series.length) {
                return renderEmptyBlock("暂无趋势数据。");
            }

            var values = series.map(function (item) {
                return Number(item.value) || 0;
            });
            var width = 760;
            var height = 280;
            var paddingX = 22;
            var paddingY = 28;
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
                    '" fill="none" stroke="#2f6b63" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"></polyline>' +
                    values
                        .map(function (_, index) {
                            var point = points.split(" ")[index].split(",");
                            return (
                                '<circle cx="' +
                                point[0] +
                                '" cy="' +
                                point[1] +
                                '" r="5" fill="#ffffff" stroke="#2f6b63" stroke-width="2"></circle>'
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

        function buildSparklineGeometry(values, options) {
            var settings = options || {};
            var width = settings.width || 760;
            var height = settings.height || 280;
            var paddingX = settings.paddingX || 22;
            var paddingY = settings.paddingY || 28;
            var baselineY = height - paddingY;
            var chartWidth = width - paddingX * 2;
            var chartHeight = height - paddingY * 2;
            var denominator = values.length > 1 ? values.length - 1 : 1;
            var maxValue = Math.max.apply(null, values);
            var minValue = Math.min.apply(null, values);
            var hasFlatSeries = maxValue === minValue;
            var flatLineY = maxValue > 0 ? baselineY - chartHeight / 2 : baselineY;

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
                    ? '<button type="button" class="analytics-action" data-overview-action="retry">重新获取</button>'
                    : "");
        }

        function resizeCharts() {
            Object.keys(chartRegistry).forEach(function (key) {
                if (chartRegistry[key] && typeof chartRegistry[key].resize === "function") {
                    chartRegistry[key].resize();
                }
            });
        }

        function disposeCharts() {
            disposeChart("trend");
            disposeChart("share");
        }

        function disposeChart(key) {
            if (chartRegistry[key] && typeof chartRegistry[key].dispose === "function") {
                chartRegistry[key].dispose();
            }
            chartRegistry[key] = null;
        }

        function isOverviewEmpty(payload) {
            return (
                !hasUsefulContent(payload.metrics) &&
                !hasUsefulContent(payload.trends) &&
                !hasUsefulContent(payload.category_share) &&
                !hasUsefulContent(payload.hot_products) &&
                !hasUsefulContent(payload.alerts)
            );
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
            return hasOwn(value, "date") && hasOwn(value, "value") && Object.keys(value).length === 2;
        }

        function isNamedMetric(value) {
            return hasOwn(value, "name") && hasOwn(value, "value") && Object.keys(value).length === 2;
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

        function sharePercentage(value, totalValue) {
            var numericValue = Number(value) || 0;
            var total = Number(totalValue) || 0;
            if (!total || !numericValue) {
                return 0;
            }
            return Number(((numericValue / total) * 100).toFixed(2));
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

        function formatCompactNumber(value) {
            var amount = Number(value) || 0;
            if (Math.abs(amount) >= 10000) {
                return (amount / 10000).toFixed(1) + "万";
            }
            return formatNumber(amount);
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

        function debounce(callback, wait) {
            var timer = null;
            return function () {
                if (timer) {
                    window.clearTimeout(timer);
                }
                timer = window.setTimeout(callback, wait);
            };
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

(function (root) {
    var doc = root.document || (typeof document !== "undefined" ? document : null);

    function onReady(callback) {
        if (!doc) {
            return;
        }
        if (doc.readyState === "loading") {
            doc.addEventListener("DOMContentLoaded", callback);
            return;
        }
        callback();
    }

    function escapeHtml(value) {
        return String(value === null || value === undefined ? "" : value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\"/g, "&quot;")
            .replace(/'/g, "&#39;");
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

    function renderPanelShell(eyebrow, title, caption, bodyHtml) {
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

    function renderNoteItem(label, value) {
        return (
            "<li><span>" +
            escapeHtml(label) +
            "</span><strong>" +
            escapeHtml(value) +
            "</strong></li>"
        );
    }

    function getSeriesLabel(item) {
        if (!item || !item.date) {
            return "暂无";
        }
        return String(item.date).slice(5).replace("-", ".");
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
            pointList: pointList,
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

    function renderSparkline(series, options) {
        var settings = options || {};
        if (!Array.isArray(series) || !series.length) {
            return renderEmptyBlock(settings.emptyText || "暂无趋势数据。");
        }

        var values = series.map(function (item) {
            return Number(item.value) || 0;
        });
        var width = settings.width || 520;
        var height = settings.height || 180;
        var sparklineGeometry = buildSparklineGeometry(values, settings);
        var points = sparklineGeometry.points;
        var areaPoints = sparklineGeometry.areaPoints;
        var pointList = sparklineGeometry.pointList;

        return (
            '<svg class="sparkline-chart" viewBox="0 0 ' +
                width +
                " " +
                height +
                '" role="img" aria-label="' +
                escapeHtml(settings.ariaLabel || "趋势图") +
                '">' +
                '<polygon points="' +
                areaPoints +
                '" fill="' +
                escapeHtml(settings.fillColor || "rgba(47, 107, 99, 0.10)") +
                '" stroke="none"></polygon>' +
                '<polyline points="' +
                points +
                '" fill="none" stroke="' +
                escapeHtml(settings.strokeColor || "#2f6b63") +
                '" stroke-width="' +
                escapeHtml(settings.lineWidth || 3) +
                '" stroke-linecap="round" stroke-linejoin="round"></polyline>' +
                pointList
                    .map(function (point) {
                        return (
                            '<circle cx="' +
                            point.x +
                            '" cy="' +
                            point.y +
                            '" r="' +
                            escapeHtml(settings.dotRadius || 4) +
                            '" fill="#ffffff" stroke="' +
                            escapeHtml(settings.strokeColor || "#2f6b63") +
                            '" stroke-width="2"></circle>'
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

    function createStatusUpdater(statusElement, options) {
        var settings = options || {};
        if (!statusElement) {
            return function () {};
        }

        return function setStatus(kind, title, description, showAction) {
            var className = settings.baseClass || "analytics-status";
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
                (showAction
                    ? '<button type="button" class="analytics-action" ' +
                        escapeHtml(settings.actionAttribute || "data-analytics-action") +
                        '="' +
                        escapeHtml(settings.actionValue || "retry") +
                        '">' +
                        escapeHtml(settings.actionLabel || "重新获取") +
                        "</button>"
                    : "");
        };
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

    function debounce(callback, wait) {
        var timer = null;
        return function () {
            var clear = root.clearTimeout || clearTimeout;
            var schedule = root.setTimeout || setTimeout;
            if (timer) {
                clear(timer);
            }
            timer = schedule(callback, wait);
        };
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

    function hasOwn(value, key) {
        return Object.prototype.hasOwnProperty.call(value, key);
    }

    root.AdminAnalyticsShared = {
        onReady: onReady,
        escapeHtml: escapeHtml,
        formatCurrency: formatCurrency,
        formatNumber: formatNumber,
        sortItems: sortItems,
        renderPanelShell: renderPanelShell,
        renderKpiCard: renderKpiCard,
        renderEmptyBlock: renderEmptyBlock,
        renderBarList: renderBarList,
        renderNoteItem: renderNoteItem,
        getSeriesLabel: getSeriesLabel,
        buildSparklineGeometry: buildSparklineGeometry,
        renderSparkline: renderSparkline,
        createStatusUpdater: createStatusUpdater,
        hasUsefulContent: hasUsefulContent,
        debounce: debounce,
    };
})(typeof window !== "undefined" ? window : globalThis);

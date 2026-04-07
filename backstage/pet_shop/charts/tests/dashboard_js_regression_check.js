const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const dashboardScriptPath = path.join(
    __dirname,
    "../../pet_shop/static/admin_analytics/dashboard.js"
);
const dashboardSource = fs.readFileSync(dashboardScriptPath, "utf8");

class FakeElement {
    constructor(attributes) {
        this.attributes = Object.assign({}, attributes);
        this.className = "";
        this.innerHTML = "";
        this.listeners = {};
    }

    addEventListener(eventName, handler) {
        this.listeners[eventName] = handler;
    }

    getAttribute(name) {
        return this.attributes[name];
    }

    setAttribute(name, value) {
        this.attributes[name] = String(value);
    }
}

function buildSeries(length, value) {
    return Array.from({ length: length }, function (_, index) {
        return {
            date: "2026-04-" + String(index + 1).padStart(2, "0"),
            value: value,
        };
    });
}

function createHarness(payload) {
    const elements = {
        page: new FakeElement({ "data-dashboard-url": "/admin/charts/dashboard/" }),
        status: new FakeElement(),
        root: new FakeElement(),
        operations: new FakeElement(),
        catalog: new FakeElement(),
        users: new FakeElement(),
        orders: new FakeElement(),
    };

    const document = {
        readyState: "complete",
        addEventListener() {},
        querySelector(selector) {
            return selector === ".admin-analytics-page" ? elements.page : null;
        },
        getElementById(id) {
            const byId = {
                "dashboard-status": elements.status,
                "analytics-dashboard-root": elements.root,
                "operations-panel": elements.operations,
                "catalog-panel": elements.catalog,
                "users-panel": elements.users,
                "orders-panel": elements.orders,
            };
            return byId[id] || null;
        },
    };

    const window = {
        document: document,
        fetch() {
            return Promise.resolve({
                ok: true,
                json() {
                    return Promise.resolve(payload);
                },
            });
        },
    };

    return { document, elements, window };
}

function flushPromises() {
    return new Promise(function (resolve) {
        setImmediate(resolve);
    });
}

async function runDashboard(payload) {
    const harness = createHarness(payload);
    vm.runInNewContext(dashboardSource, {
        console,
        document: harness.document,
        setImmediate,
        setTimeout,
        clearTimeout,
        window: harness.window,
    });

    await flushPromises();
    await flushPromises();

    return harness.elements;
}

function extractPolylineYValues(panelHtml) {
    const matches = Array.from(panelHtml.matchAll(/<polyline points="([^"]+)"/g));
    return matches.map(function (match) {
        return match[1].split(" ").map(function (pair) {
            return Number(pair.split(",")[1]);
        });
    });
}

async function main() {
    const blankElements = await runDashboard({
        sections: {
            operations: {
                gmv: 0,
                order_count: 0,
                average_order_value: 0,
                payment_method_distribution: [],
            },
            catalog: {
                category_share: [],
                price_band_distribution: [],
                hot_products: [],
                low_stock_products: [],
            },
            users: {
                new_user_trend: {
                    "7d": buildSeries(7, 0),
                    "30d": buildSeries(30, 0),
                },
                province_distribution: [],
                rating_summary: {
                    total_comments: 0,
                    average_rating: "0.00",
                    distribution: [],
                },
            },
            orders: {
                status_distribution: [],
                refund_distribution: [],
                sales_trend: {
                    "7d": buildSeries(7, 0),
                    "30d": buildSeries(30, 0),
                },
                order_trend: {
                    "7d": buildSeries(7, 0),
                    "30d": buildSeries(30, 0),
                },
            },
        },
    });

    assert.equal(
        blankElements.root.attributes["data-state"],
        "empty",
        "blank zero-filled trend data should render the dashboard empty state"
    );

    const sparklineElements = await runDashboard({
        sections: {
            operations: {
                gmv: 1280,
                order_count: 16,
                average_order_value: 80,
                payment_method_distribution: [{ name: "微信支付", value: 16 }],
            },
            catalog: {
                category_share: [],
                price_band_distribution: [],
                hot_products: [],
                low_stock_products: [],
            },
            users: {
                new_user_trend: {
                    "7d": buildSeries(7, 1),
                    "30d": buildSeries(30, 2),
                },
                province_distribution: [],
                rating_summary: {
                    total_comments: 0,
                    average_rating: "0.00",
                    distribution: [],
                },
            },
            orders: {
                status_distribution: [{ name: "已完成", value: 16 }],
                refund_distribution: [],
                sales_trend: {
                    "7d": buildSeries(7, 5),
                    "30d": buildSeries(30, 5),
                },
                order_trend: {
                    "7d": buildSeries(7, 0),
                    "30d": buildSeries(30, 0),
                },
            },
        },
    });

    const sparklineSeries = extractPolylineYValues(sparklineElements.orders.innerHTML);
    assert.equal(sparklineSeries.length, 2, "orders panel should render two sparkline charts");
    assert.notDeepEqual(
        sparklineSeries[0],
        sparklineSeries[1],
        "constant positive trend should not render identically to an all-zero trend"
    );
    assert.ok(
        sparklineSeries[0].every(function (value) {
            return value < 160;
        }),
        "constant positive trend should render above the zero baseline"
    );

    console.log("dashboard_js_regression_check: ok");
}

main().catch(function (error) {
    console.error(error && error.stack ? error.stack : error);
    process.exitCode = 1;
});

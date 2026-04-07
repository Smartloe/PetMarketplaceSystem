const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const overviewScriptPath = path.join(
    __dirname,
    "../../pet_shop/static/admin_analytics/overview.js"
);
const sharedScriptPath = path.join(
    __dirname,
    "../../pet_shop/static/admin_analytics/shared.js"
);
const sharedSource = fs.readFileSync(sharedScriptPath, "utf8");
const overviewSource = fs.readFileSync(overviewScriptPath, "utf8");

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

    closest() {
        return null;
    }
}

class FakeTrigger {
    constructor(selector, attributes) {
        this.selector = selector;
        this.attributes = Object.assign({}, attributes);
    }

    closest(selector) {
        return selector === this.selector ? this : null;
    }

    getAttribute(name) {
        return this.attributes[name];
    }
}

function buildSeries(length, valueFactory) {
    return Array.from({ length: length }, function (_, index) {
        return {
            date: "2026-04-" + String(index + 1).padStart(2, "0"),
            value:
                typeof valueFactory === "function"
                    ? valueFactory(index)
                    : valueFactory,
        };
    });
}

function createHarness(fetchImpl) {
    const elements = {
        page: new FakeElement({ "data-overview-url": "/api/charts/overview/" }),
        status: new FakeElement(),
        root: new FakeElement(),
        metrics: new FakeElement(),
        trend: new FakeElement(),
        share: new FakeElement(),
        hotProducts: new FakeElement(),
        alerts: new FakeElement(),
    };

    const document = {
        readyState: "complete",
        addEventListener() {},
        querySelector(selector) {
            return selector === ".admin-overview" ? elements.page : null;
        },
        getElementById(id) {
            const byId = {
                "overview-status": elements.status,
                "admin-overview-root": elements.root,
                "overview-metrics": elements.metrics,
                "overview-trend-chart": elements.trend,
                "overview-share-chart": elements.share,
                "overview-hot-products": elements.hotProducts,
                "overview-alerts": elements.alerts,
            };
            return byId[id] || null;
        },
    };

    const window = {
        document: document,
        fetch: fetchImpl,
        addEventListener() {},
        clearTimeout,
        setTimeout,
    };

    return { document, elements, window };
}

function flushPromises() {
    return new Promise(function (resolve) {
        setImmediate(resolve);
    });
}

async function bootOverview(fetchImpl) {
    const harness = createHarness(fetchImpl);
    const context = {
        console,
        document: harness.document,
        setImmediate,
        setTimeout,
        clearTimeout,
        window: harness.window,
    };

    vm.runInNewContext(sharedSource, context);
    assert.ok(
        harness.window.AdminAnalyticsShared,
        "shared analytics helper should be available before overview.js executes"
    );
    vm.runInNewContext(overviewSource, context);

    await flushPromises();
    await flushPromises();

    return harness;
}

async function main() {
    const blankHarness = await bootOverview(function () {
        return Promise.resolve({
            ok: true,
            json() {
                return Promise.resolve({
                    metrics: {
                        gmv: "0.00",
                        order_count: 0,
                        new_users_count: 0,
                        low_stock_count: 0,
                    },
                    trends: {
                        sales: {
                            "7d": buildSeries(7, 0),
                            "30d": buildSeries(30, 0),
                        },
                        orders: {
                            "7d": buildSeries(7, 0),
                            "30d": buildSeries(30, 0),
                        },
                    },
                    category_share: [],
                    hot_products: [],
                    alerts: [],
                });
            },
        });
    });

    assert.equal(
        blankHarness.elements.root.attributes["data-state"],
        "empty",
        "blank overview payload should render the empty state"
    );
    assert.match(
        blankHarness.elements.trend.innerHTML,
        /暂无趋势数据/,
        "blank overview payload should not pretend trend content exists"
    );

    const errorHarness = await bootOverview(function () {
        return Promise.reject(new Error("network down"));
    });

    assert.equal(
        errorHarness.elements.root.attributes["data-state"],
        "error",
        "fetch failures should render the error state"
    );
    assert.match(
        errorHarness.elements.status.innerHTML,
        /data-overview-action="retry"/,
        "fetch failures should render a retry affordance"
    );

    const interactiveHarness = await bootOverview(function () {
        return Promise.resolve({
            ok: true,
            json() {
                return Promise.resolve({
                    metrics: {
                        gmv: "1500.00",
                        order_count: 18,
                        new_users_count: 5,
                        low_stock_count: 2,
                    },
                    trends: {
                        sales: {
                            "7d": buildSeries(7, function (index) {
                                return 100 + index * 10;
                            }),
                            "30d": buildSeries(30, function (index) {
                                return 400 + index * 20;
                            }),
                        },
                        orders: {
                            "7d": buildSeries(7, function (index) {
                                return 1 + index;
                            }),
                            "30d": buildSeries(30, function (index) {
                                return 10 + index;
                            }),
                        },
                    },
                    category_share: [{ name: "主粮", value: 12 }],
                    hot_products: [
                        {
                            title: "冻干主粮",
                            sold_quantity: 9,
                            stock_quantity: 4,
                        },
                    ],
                    alerts: [
                        {
                            level: "warning",
                            title: "低库存提醒",
                            description: "测试提醒",
                            target_url: "/admin/commodity/commodityinfos/",
                        },
                    ],
                });
            },
        });
    });

    assert.match(
        interactiveHarness.elements.trend.innerHTML,
        /当前指标<\/span><strong>销售额/,
        "overview should render the default sales metric"
    );
    assert.match(
        interactiveHarness.elements.trend.innerHTML,
        /最近一天<\/span><strong>¥980.00/,
        "overview should render the default 30d latest sales value"
    );

    interactiveHarness.elements.page.listeners.click({
        preventDefault() {},
        target: new FakeTrigger("[data-overview-metric]", {
            "data-overview-metric": "orders",
        }),
    });
    interactiveHarness.elements.page.listeners.click({
        preventDefault() {},
        target: new FakeTrigger("[data-overview-window]", {
            "data-overview-window": "7d",
        }),
    });

    assert.match(
        interactiveHarness.elements.trend.innerHTML,
        /当前指标<\/span><strong>订单量/,
        "metric toggle should re-render the trend panel"
    );
    assert.match(
        interactiveHarness.elements.trend.innerHTML,
        /最近一天<\/span><strong>7<\/strong>/,
        "window toggle should update the latest rendered value without crashing"
    );

    console.log("overview_js_regression_check: ok");
}

main().catch(function (error) {
    console.error(error && error.stack ? error.stack : error);
    process.exitCode = 1;
});

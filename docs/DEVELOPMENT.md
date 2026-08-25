# 吉祥宠物商城 开发文档

面向要在本地跑起来并改代码的开发者。接口的字段级细节请直接看运行中的
`/swagger/` 或 `/redoc/`，本文不重复抄一遍。

## 1. 环境准备

必需：

- **Python 3.12**。不是 3.13 —— `pillow==10.3.0` 在 3.13 上编译不过，
  所有 `uv` 命令都要显式带 `--python 3.12`。
- Node.js 16+
- MySQL 8.0+
- `uv`（`pip install uv`）

### 后端

```bash
cd backstage/pet_shop
cp .env.template .env        # 然后按第 2 节填写
uv sync --python 3.12
uv run --python 3.12 python manage.py migrate
uv run --python 3.12 python manage.py createsuperuser
uv run --python 3.12 python manage.py runserver 127.0.0.1:8000
```

建库语句（`.env` 里的 `MYSQL_DATABASE` 默认是 `pet_shop`）：

```sql
CREATE DATABASE pet_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

可选：写入演示业务数据，让后台概览和分析页有内容。该命令**只在
`DEBUG=True` 时允许执行**，否则直接报 `CommandError`。

```bash
uv run --python 3.12 python manage.py seed_demo_business_data
```

### 前端

```bash
cd frontstage/pet_shop
npm install
npm run serve      # 端口 8010
```

开发服务器跑在 **8010**，`vue.config.js` 把 `/api` 代理到
`http://127.0.0.1:8000`。后端的 `CORS_ALLOWED_ORIGINS` 与
`CSRF_TRUSTED_ORIGINS` 默认值也是 8010 的两个来源，改前端端口时这两个都要跟着改。

访问地址：

| 用途 | 地址 |
| --- | --- |
| 前台 | http://127.0.0.1:8010 |
| 后台管理 | http://127.0.0.1:8000/admin/ |
| Swagger | http://127.0.0.1:8000/swagger/ |
| ReDoc | http://127.0.0.1:8000/redoc/ |

## 2. 环境变量

全部配置走 `.env`（已 gitignore）。模板 `backstage/pet_shop/.env.template`
是提交进仓库的，列了每一个变量。`settings.py` 里不再有硬编码的
SECRET_KEY 或数据库密码。

| 变量 | 说明 |
| --- | --- |
| `DJANGO_SECRET_KEY` | `DJANGO_DEBUG=False` 时**必填**，否则启动直接抛 `ImproperlyConfigured`；DEBUG 开着时用不安全的开发兜底值 |
| `DJANGO_DEBUG` | 默认 `True` |
| `DJANGO_ALLOWED_HOSTS` | 逗号分隔，默认 `127.0.0.1,localhost` |
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DATABASE` / `MYSQL_USER` / `MYSQL_PASSWORD` | 数据库连接 |
| `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` | 显式白名单，逗号分隔。**没有通配符** |
| `LONGCAT_API_KEY` | 不配则 `/api/ai/consult/` 返回 503 |
| `LONGCAT_API_URL` | 可选，覆盖上游地址 |
| `JWT_ACCESS_MINUTES` / `JWT_REFRESH_DAYS` | 默认 60 分钟 / 7 天 |
| `THROTTLE_AI_CONSULT` / `THROTTLE_CAPTCHA` / `THROTTLE_LOGIN` | 默认 `10/min` / `30/min` / `10/min` |
| `CACHE_BACKEND` / `CACHE_LOCATION` | 见第 6 节 |
| `COMMODITY_PREVIEW_LIMIT` | 未登录用户每个分类可见的商品数，默认 6 |

`MYSQL_HOST` 不设时 `settings.detect_mysql_host()` 会探测运行环境：WSL2 下读
`/etc/resolv.conf` 的第一个 nameserver（指向 Windows 宿主），否则用
`127.0.0.1`。在 `.env` 里显式写 `MYSQL_HOST` 就会跳过这套探测。

关键的 DRF 全局设置（`settings.py`）：分页 `PAGE_SIZE = 6`，默认权限
`IsAuthenticated`，认证类是 `JWTAuthentication` + 标准
`SessionAuthentication`（后者留给 DRF 可浏览界面和后台内嵌调用）。CSRF
中间件是**开启**的。

## 3. 认证流程

前台走 JWT（`djangorestframework-simplejwt`），登录带图形验证码。

1. `GET /api/accounts/captcha/?username=X` → `{"img": "<base64 JPEG>"}`。
   **响应里没有答案**，答案存在 Django 缓存的 `verify_code_<username>` 键下，
   有效期 60 秒，且一次性使用 —— `LoginView` 无论校验成败都会立刻删掉它。
2. `POST /api/accounts/login/`，body `{username, password, code}`。成功返回：

   ```json
   {
     "status": 200,
     "message": "用户登录成功",
     "id": 1,
     "username": "demo",
     "email": "demo@example.com",
     "last_login": "2026-01-01T10:00:00",
     "access": "<JWT>",
     "refresh": "<JWT>"
   }
   ```

   `last_login` 回传的是**本次登录之前**的值。验证码错返回 400
   `{"error": "验证码无效"}`，账号密码错返回 401。
3. 前端只把 `access` / `refresh` 存进 localStorage（键名
   `access_token` / `refresh_token`），每个请求带
   `Authorization: Bearer <access>`。
4. `access` 过期后 `POST /api/accounts/token/refresh/`，body `{refresh}`。
   前端 `src/api/index.js` 的响应拦截器在收到 401 时自动刷新并重放原请求，
   并发的 401 共享同一次刷新。
5. `POST /api/accounts/token/verify/` 校验 token 有效性。
6. 登出路由是 `POST /api/accounts/loginout/`（**不是** `/logout/`）。JWT
   无状态，真正的登出动作是前端清掉本地 token。

注册是 `POST /api/accounts/register/`，字段 `username / email / password /
password2`，两次密码不一致或邮箱已注册都会 400。

## 4. 数据模型

Django 内置的 `auth.User` 就是用户主体，没有启用自定义 `AUTH_USER_MODEL`。

### commodity

- **`CommodityInfos`**：`sku_title`（商品名）、`sku_description`、
  `main_image`、`detail_images`、`cost_price`（进价）、`price`（售价）、
  `status`、`types`（外键 → `CommodityCategories`）、`sold`（已售）、
  `stock_quantity`（库存）、`created_by/created_time/updated_by/updated_time`。
- **`CommodityCategories`**：`title`（唯一）、`parent_category`（自关联，
  `related_name='sub_categories'`）。只有两层：顶级类型 + 子类型。

### trade

- **`OrderInfos`**：`user`、`order_sn`（唯一）、`address`（外键 →
  `customer_operation.UserAddress`）、`total_price`、`coupon_price`、
  `payable_price`、`pay_method`、`leave_comment`、`order_status`、
  `confirmed_time`、`refund_status`、`refund_reason`、`created_by/created_time/
  update_by/update_time`（注意订单表这两个是 `update_by`/`update_time`，
  没有 `d`）。
- **`OrderGoods`**：`order`（`related_name='goods'`）、`goods`（外键 →
  `CommodityInfos`）、`goods_num`、`add_time`、`commented`。
- **`ShoppingCart`**：`user`、`commodity`（`on_delete=SET_NULL`、
  `db_constraint=False`，所以可能为 `None`）、`quantity`、`created_time`、
  `updated_time`。

状态码取值：

| 字段 | 取值 |
| --- | --- |
| `order_status` | 0 未支付 / 1 已支付 / 2 发货中 / 3 已签收 / 4 退货中 / 5 已退货 |
| `refund_status` | 0 无 / 1 待审核 / 2 已通过 / 3 已拒绝 |
| `pay_method` | 1 微信 / 2 支付宝 / 3 银联 |

### customer_operation

- **`UserFav`**：`user` + `goods`，`unique_together`。
- **`UserLeavingMessage`**：`message_type`（1 留言 / 2 投诉 / 3 询问 /
  4 售后 / 5 求购）、`subject`、`message`、`file`、`is_replied`、
  `reply_content`、`reply_time`。
- **`UserAddress`**：`province`、`city`、`county`、`address`、`is_default`、
  `signer_name`、`signer_mobile`。排序把默认地址放最前。
- **`UserComment`**：`user`、`commodity`、`content`、`rating`（1–5，模型层有
  `MinValueValidator`/`MaxValueValidator`）、`is_show`（后台审核开关）。

### accounts

- **`UserProfile`**：`username` 是指向 `auth.User` 的外键（`to_field='username'`，
  不是字符串字段）、`birthday`、`gender`（M/F/O）、`user_intro`、`avatar`、
  `mobile`（`PhoneNumberField`，region CN）、`user_score`、`total_cost_amt`。
  首次访问个人中心时由 `UserProfileViewSet.list()` 惰性补齐。

### merchant / charts / index

- **`merchant.Advertisement`**：`ad_title`、`ad_content`、`ad_image`、
  `ad_link`、`start_date`、`end_date`、`click_count`。
- **`charts.SoldModel` / `charts.UserModel`**：只有一个 `name` 字段，纯占位，
  作用是在 Admin 菜单里挂出「综合数据看板」「用户数据可视化」两个入口。
- **`index`**：没有模型，只有 AI 咨询视图。

## 5. API 一览

前缀在 `pet_shop/urls.py` 挂载。字段细节看 `/swagger/`。

### accounts — `/api/accounts/`

`register/`、`login/`、`loginout/`、`token/refresh/`、`token/verify/`、
`captcha/`、`profiles/`（ViewSet，只返回当前用户）、
`profiles/upload-avatar/`。

### commodity — `/api/commodity/`

- `list/` — 按分类分组的商品树。匿名可访问，但每个分类只返回
  `COMMODITY_PREVIEW_LIMIT` 条，响应里带 `limited` 和 `preview_limit`。
- `detail/<pk>/` — 商品详情 + 所属分类。匿名可访问。
- `search/` — `?query=` 对 `sku_title` / `sku_description` 模糊匹配，同样有匿名限量。
- `comments/<pk>/` — 某商品的评论列表（只含 `is_show=True`）。

### trade — `/api/trade/`

ViewSet：`orders/`、`order-goods/`、`shopping-carts/`（都只返回当前用户的数据）。
`shopping-carts/` 的 POST 用 `{commodity, quantity}`，同一商品重复提交会累加数量而不是建新行。

自定义端点：

- `POST checkout/` — body `{cart_ids: [], address_id, pay_method, leave_comment}`。
  整个过程在一个事务里：`select_for_update()` 按 id 升序锁商品行 → 校验库存 →
  建单 → 扣 `stock_quantity`、加 `sold` → 清购物车。库存不够返回 400
  `库存不足：<商品名>`；下单成功返回 201 和 `order_sn`。订单初始状态是 2（发货中）。
- `POST orders/<order_id>/refund/` — body `{reason, refund_type}`。未发货
  （`order_status < 2`）、已退货、重复提交都会 400；已签收的订单超过确认收货 7 天不再受理。
- `POST orders/<order_id>/confirm/` — 确认收货，写 `confirmed_time`。
- `POST orders/<order_id>/goods/<order_goods_id>/comment/` — body
  `{content, rating}`，`rating` 必须是 1–5 的整数。订单未签收或该商品已评价会 400。

### customer_operation — `/api/operation/`

ViewSet：`favorites/`、`messages/`、`addresses/`、`usercomments/`。前三个都限定当前用户；
`usercomments/` 的读操作 `AllowAny`、写操作要求登录。另有 `regions/`（省市区级联数据，免认证）。

### merchant — `/api/merchant/`

`advertisements/` — 只读 ViewSet。

### index — `/api/ai/consult/`

`POST`，**需要登录**，限流 scope `ai_consult`（默认 10/min）。body 支持
`{messages: [{role, content}], question, stream}`。默认 `stream=True`，返回
`text/event-stream`，每帧形如 `data: {"content": "..."}`，结束帧 `data: {"done": true}`；
`stream=False` 时返回 `{answer, usage}`。

服务端约束：模型固定 `LongCat-Flash-Chat`，`max_tokens=1200`、
`temperature=0.7`，**请求体里的同名字段一律忽略**；单条内容超过 2000 字返回 400；
只保留最近 8 轮对话；命中非宠物话题时不调上游，直接返回引导话术。未配
`LONGCAT_API_KEY` 返回 503。

### charts — `/api/charts/`

`overview/`、`dashboard/`。两个都是 `@staff_member_required` 的普通 Django
视图（返回 `JsonResponse`），不是 DRF 端点 —— 未登录会被重定向到 admin 登录页，
而不是返回 401。

## 6. 已知注意事项

**LocMemCache 与验证码。** 缓存默认是
`django.core.cache.backends.locmem.LocMemCache`，**不是 Redis**。它是每进程独立的，
而验证码答案就存在缓存里。单进程 `runserver` 没问题，但一旦多 worker
（gunicorn/uwsgi）或多机部署，验证码就会随机报「验证码无效」—— 生成和校验落在了不同进程。
上线前用 `CACHE_BACKEND` / `CACHE_LOCATION` 换成 Redis 或 Memcached。

**`pet_shop_backup.sql` 用不了。** 该文件已从 git 移除，`*.sql` 也进了
`.gitignore`（导出文件含真实用户数据：密码哈希、邮箱、手机号）。即使你手上有这个文件，
它也**无法直接导入**：编码是 UTF-16LE，中文内容是乱码，并且有一处未转义的引号会让
`mysql` 客户端报语法错误。**唯一受支持的建数据路径是 `migrate` +
`seed_demo_business_data`。**

导出数据库时不要把密码写进命令（会留在 shell 历史里）：

```bash
mysqldump -u root -p pet_shop > pet_shop_backup.sql
```

**后台图表的 ECharts 来自 CDN。** `templates/admin/index.html` 里通过
`<script src="https://fastly.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js">`
引入，Python 侧没有任何图表库（`pyecharts`、`django-echarts`、`django-chartjs`
都已移除）。离线环境下后台图表会渲染不出来。

**依赖已精简到 14 个直接依赖**，见 `pyproject.toml`，传递依赖由 `uv.lock` 锁定。
已移除：两个 alipay SDK、`django-jazzmin`、`django-grappelli`、`django-chartjs`、
`django-echarts`、`echarts-python`、`pyecharts`。`INSTALLED_APPS` 里的后台皮肤只有
`simpleui`。

**前端有两套 axios 配置。** `src/api/index.js` 是主要的那套（JWT 拦截器 +
自动刷新，baseURL 走 `/api` 代理）；`src/axios/index.js` 是另一份带 CSRF 头处理、
baseURL 硬编码为 `http://localhost:8010/api/` 的实例。新代码用前者。

## 7. 测试

```bash
cd backstage/pet_shop
uv run --python 3.12 python manage.py test
```

当前 **52 个测试全部通过**。测试集中在 `charts/tests/`（分析服务、seed 命令、
admin 视图、端到端 smoke），其余 app 的 `tests.py` 多为空壳。

前端只有 ESLint，没有单元测试：

```bash
cd frontstage/pet_shop
npm run lint
```

## 8. 排查

**前端能打开但没数据**：确认后端在 `127.0.0.1:8000`、前端在 `8010`、
`/api` 代理生效、数据库已 `migrate`（需要演示数据就跑 `seed_demo_business_data`）。

**后台图表空白**：确认跑过 `seed_demo_business_data`、当前账号是
staff（`/api/charts/` 两个端点要求 `staff_member_required`）、能访问 jsdelivr CDN。

**登录一直提示验证码无效**：验证码只有 60 秒且一次性；每次提交前重新拉一张图。
如果是多进程部署，看第 6 节的 LocMemCache 问题。

**`uv sync` 编译 pillow 失败**：用的是 Python 3.13。加 `--python 3.12`。

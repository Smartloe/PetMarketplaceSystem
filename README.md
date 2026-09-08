# 吉祥宠物商城系统

[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Smartloe/PetMarketplaceSystem)

一个前后端分离的宠物商城项目，包含用户注册登录、商品浏览、购物车、订单、留言、AI 宠物顾问，以及基于 Django Admin 的综合后台与数据看板。

## 项目亮点

- 前台商城：商品列表、详情、收藏、购物车、下单、售后与个人中心。
- AI 宠物顾问：通过 `/api/ai/consult/` 提供宠物问答能力。
- 后台管理：商品、订单、广告、用户、评论等模块集中管理。
- 数据可视化：后台首页提供简版经营概览，分析页提供完整图表。
- 演示数据：支持把假数据写入真实业务表，便于本地演示和联调。

## 技术栈

### 前端

- Vue 3
- Vue Router
- Vuex
- Element Plus
- Axios
- Vue CLI

### 后端

- Django 5
- Django REST Framework
- SimpleUI
- MySQL
- uv
- drf-yasg

## 目录结构

```text
PetMarketplaceSystem/
├── backstage/
│   └── pet_shop/
│       ├── accounts/                # 账户与用户资料
│       ├── charts/                  # 后台概览与分析接口、演示数据
│       ├── commodity/               # 商品与分类
│       ├── customer_operation/      # 地址、收藏、留言、评论
│       ├── index/                   # 首页与 AI 相关接口
│       ├── merchant/                # 广告与商家数据
│       ├── trade/                   # 购物车、订单、退款、确认收货
│       ├── pet_shop/                # Django 配置、静态资源
│       ├── templates/               # Admin 模板覆盖
│       ├── manage.py
│       ├── pyproject.toml
│       └── uv.lock
├── frontstage/
│   └── pet_shop/
│       ├── public/
│       ├── src/
│       │   ├── api/
│       │   ├── assets/
│       │   ├── components/
│       │   ├── router/
│       │   ├── store/
│       │   └── views/
│       ├── package.json
│       └── vite.config.js
└── README.md
```

## 环境要求

- **Python 3.12**（不要用 3.13：`pillow==10.3.0` 在 3.13 上编译不过，所以下面所有 `uv` 命令都显式带 `--python 3.12`）
- Node.js 16+
- MySQL 8.0+
- Git
- uv

安装 `uv`：

```bash
pip install uv
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Smartloe/PetMarketplaceSystem.git
cd PetMarketplaceSystem
```

### 2. 准备数据库

先创建数据库：

```sql
CREATE DATABASE pet_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

所有配置都走 `.env`（已 gitignore）。仓库里提交了 `.env.template`，列出了每一个可用变量：

```bash
cd backstage/pet_shop
cp .env.template .env
```

然后按需填写，常用的几项：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=pet_shop
MYSQL_USER=root
MYSQL_PASSWORD=your_password
LONGCAT_API_KEY=your_longcat_api_key
```

`settings.py` 里已经不含 SECRET_KEY 和数据库密码。`DJANGO_DEBUG=False` 时
`DJANGO_SECRET_KEY` 是**必填**的，否则启动会直接失败；开发环境（DEBUG=True）可以留空。
数据库名不填默认就是 `pet_shop`。

### 4. 启动后端

```bash
cd backstage/pet_shop
uv sync --python 3.12
uv run --python 3.12 python manage.py migrate
uv run --python 3.12 python manage.py createsuperuser
uv run --python 3.12 python manage.py runserver 127.0.0.1:8000
```

可选：写入演示业务数据，方便查看后台概览和完整分析页。该命令只在 `DEBUG=True` 时可用。

```bash
uv run --python 3.12 python manage.py seed_demo_business_data
```

### 5. 启动前端

```bash
cd frontstage/pet_shop
npm install
npm run serve
```

前端开发服务器默认端口是 `8010`，并通过 `vite.config.js` 将 `/api` 代理到 `http://127.0.0.1:8000`。
后端的 `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` 默认值也是 8010 的两个来源，改端口时要同步改。

### 6. 访问地址

- 前台首页：http://127.0.0.1:8010
- 后台管理：http://127.0.0.1:8000/admin/
- Swagger 文档：http://127.0.0.1:8000/swagger/
- ReDoc 文档：http://127.0.0.1:8000/redoc/

## 数据库初始化与导出

### 如何得到一份可用的数据

用迁移建表，再按需写入演示数据：

```bash
cd backstage/pet_shop
uv run --python 3.12 python manage.py migrate
uv run --python 3.12 python manage.py seed_demo_business_data
```

这是本项目**唯一受支持**的建数据方式。

仓库里那份 `pet_shop_backup.sql` 已经不再纳入版本管理（`*.sql` 已加入 `.gitignore`，
导出文件含真实用户数据：密码哈希、邮箱、手机号）。即使你手上有这个文件，它也无法直接导入 ——
编码是 UTF-16LE、中文是乱码，并且有一处未转义的引号会让 `mysql` 客户端报语法错误。

### 使用 mysqldump 导出数据库

不要把密码写在命令里（会留在 shell 历史中），用 `-p` 让它交互式提示：

```bash
mysqldump -u root -p pet_shop > pet_shop_backup.sql
```

## 常用开发命令

### 后端

```bash
cd backstage/pet_shop

# 安装或同步依赖
uv sync --python 3.12

# 数据库迁移
uv run --python 3.12 python manage.py makemigrations
uv run --python 3.12 python manage.py migrate

# 创建管理员
uv run --python 3.12 python manage.py createsuperuser

# 写入演示数据（仅 DEBUG=True 可用）
uv run --python 3.12 python manage.py seed_demo_business_data

# 运行测试（当前 52 个全部通过）
uv run --python 3.12 python manage.py test

# 本地启动
uv run --python 3.12 python manage.py runserver 127.0.0.1:8000
```

### 前端

```bash
cd frontstage/pet_shop

# 安装依赖
npm install

# 本地开发
npm run serve

# 生产构建
npm run build

# 代码检查
npm run lint
```

## 主要功能模块

### 前台

- 首页推荐与广告位
- 商品列表、详情、搜索与分类筛选
- 购物车与订单结算
- 收藏、留言、评论、地址管理
- AI 宠物顾问

### 后台

- 商品管理与库存管理
- 订单管理、退款审核、确认收货
- 广告管理
- 用户与用户资料管理
- 后台首页经营概览
- 完整数据分析页

## 关键接口

### 业务接口

- `/api/accounts/`：注册、登录、登出、用户资料
- `/api/commodity/`：商品列表 `list/`、详情 `detail/<id>/`、搜索 `search/`、评论 `comments/<id>/`
- `/api/trade/`：购物车 `shopping-carts/`、订单 `orders/`、结算 `checkout/`、退款、确认收货、评价
- `/api/operation/`：收藏、留言、地址、评论、省市区数据
- `/api/merchant/`：广告位（只读）
- `/api/ai/consult/`：AI 宠物顾问，**需要登录**并有限流（默认 10 次/分钟）

### 认证接口

前台使用 JWT：

- `GET /api/accounts/captcha/?username=X`：获取图形验证码，只返回图片（`{img}`），答案留在服务端缓存，60 秒有效且一次性使用
- `POST /api/accounts/login/`：body `{username, password, code}`，返回 `access` / `refresh`
- `POST /api/accounts/token/refresh/`：body `{refresh}`，用于 `access` 过期后换新的
- `POST /api/accounts/token/verify/`：校验 token
- `POST /api/accounts/loginout/`：登出（注意路由是 `loginout`，不是 `logout`）

前端只在 localStorage 保存 `access_token` / `refresh_token`，请求统一带
`Authorization: Bearer <access>`，并在收到 401 时自动刷新重放。

### 后台分析接口

- `/api/charts/overview/`：后台首页概览数据
- `/api/charts/dashboard/`：完整分析页数据

## 后台说明

- 后台首页是“先扫一眼”的总控台，集中展示近 30 天核心指标、走势、分类热度、热销商品和待处理提醒。
- 后台分析页提供更完整的图表与明细。
- 后台 Logo 已与前台品牌统一。
- 数据可视化支持基于真实业务表的演示数据，不依赖单独的 mock 文件。

## 故障排查

### 前端能打开但看不到数据

优先检查：

1. 后端是否运行在 `127.0.0.1:8000`
2. 前端是否通过 `npm run serve` 启动在 `8010`
3. `vite.config.js` 中 `/api` 代理是否生效
4. 是否执行过 `migrate`，需要演示数据时是否跑过 `seed_demo_business_data`
5. `CORS_ALLOWED_ORIGINS` 是否包含前端来源

### 后台图表没有数据

可按顺序检查：

1. 是否执行过 `uv run --python 3.12 python manage.py seed_demo_business_data`
2. 当前登录账号是否为后台管理员（`/api/charts/` 的两个接口要求 staff 权限）
3. 网络能否访问 jsDelivr —— 后台图表的 ECharts 是从 CDN 引入的，离线环境下会渲染不出来

### `uv sync` 编译 pillow 失败

用的是 Python 3.13。加上 `--python 3.12`。

### 登录总提示验证码无效

验证码只有 60 秒有效期且一次性使用，每次提交前重新获取一张。多进程部署时还需注意：
缓存默认是 LocMemCache（每进程独立），验证码会因为生成和校验落在不同进程而失效，
这种情况下需要通过 `CACHE_BACKEND` / `CACHE_LOCATION` 换成 Redis。

## 许可证

本项目使用 [MIT License](LICENSE)。

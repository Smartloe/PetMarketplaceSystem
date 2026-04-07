# 吉祥宠物商城系统

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
│       └── vue.config.js
└── README.md
```

## 环境要求

- Python 3.10+
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

项目后端默认读取这些环境变量：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=pet_shop
MYSQL_USER=root
MYSQL_PASSWORD=your_password
LONGCAT_API_KEY=your_longcat_api_key
```

如果不额外配置，开发环境默认数据库名就是 `pet_shop`。

### 3. 启动后端

```bash
cd backstage/pet_shop
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 127.0.0.1:8000
```

可选：写入演示业务数据，方便查看后台概览和完整分析页。

```bash
uv run python manage.py seed_demo_business_data
```

### 4. 启动前端

```bash
cd frontstage/pet_shop
npm install
npm run serve
```

前端开发服务器默认端口是 `8010`，并通过 `vue.config.js` 将 `/api` 代理到 `http://127.0.0.1:8000`。

### 5. 访问地址

- 前台首页：http://127.0.0.1:8010
- 后台管理：http://127.0.0.1:8000/admin/
- Swagger 文档：http://127.0.0.1:8000/swagger/
- ReDoc 文档：http://127.0.0.1:8000/redoc/

## 数据库导入与导出

### 导入已有备份

如果你已经有 `pet_shop_backup.sql`：

```bash
mysql -u root -p pet_shop < pet_shop_backup.sql
```

### 使用 mysqldump 导出数据库

本地开发机可直接使用：

```bash
mysqldump -u root -pxllzy123 pet_shop > pet_shop_backup.sql
```

更安全的写法是不要把真实密码直接写进命令历史，而是使用交互输入：

```bash
mysqldump -u root -p pet_shop > pet_shop_backup.sql
```

## 常用开发命令

### 后端

```bash
cd backstage/pet_shop

# 安装或同步依赖
uv sync

# 数据库迁移
uv run python manage.py makemigrations
uv run python manage.py migrate

# 创建管理员
uv run python manage.py createsuperuser

# 写入演示数据
uv run python manage.py seed_demo_business_data

# 运行测试
uv run python manage.py test

# 本地启动
uv run python manage.py runserver 127.0.0.1:8000
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

- `/api/accounts/`
- `/api/commodity/`
- `/api/trade/`
- `/api/operation/`
- `/api/merchant/`
- `/api/ai/consult/`

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
3. `vue.config.js` 中 `/api` 代理是否生效
4. MySQL 是否已导入数据或执行过 `seed_demo_business_data`

### 后台图表没有数据

可按顺序检查：

1. 是否已导入 `pet_shop_backup.sql`
2. 是否执行过 `uv run python manage.py seed_demo_business_data`
3. 当前登录账号是否为后台管理员

## 许可证

本项目使用 [MIT License](LICENSE)。

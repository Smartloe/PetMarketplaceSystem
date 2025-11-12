# 基于Django的宠物商城设计与实现

## 后端（Django）

本项目的后端依赖现在由 [uv](https://github.com/astral-sh/uv) 负责管理，已在 `backstage/pet_shop/pyproject.toml` 中声明所有第三方库。常用命令（需在 `backstage/pet_shop` 目录中执行）：

```bash
# 安装依赖并创建虚拟环境（.venv）
uv sync

# 启动开发服务器（根据需要设置数据库环境变量，见下方）
uv run python manage.py runserver 0.0.0.0:8000

# 运行数据库迁移
uv run python manage.py migrate
```

### 数据库连接（WSL 访问 Windows MySQL）

后端运行在 WSL，而 MySQL 位于 Windows，需要注意以下事项：

1. **允许 Windows MySQL 被外部访问**
	- 在 `my.ini` / `my.cnf` 中将 `bind-address` 改为 `0.0.0.0`，并创建对外账号：
		```sql
		CREATE USER 'root'@'%' IDENTIFIED BY '你的密码';
		GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
		FLUSH PRIVILEGES;
		```
	- Windows 防火墙放行 3306 端口：
		```powershell
		netsh advfirewall firewall add rule name="MySQL 3306" dir=in action=allow protocol=TCP localport=3306
		```
2. **在 WSL 内指定连接信息**
		- 项目会自动检测 WSL 环境并优先使用 `/etc/resolv.conf` 中的 `nameserver` IP（通常即 Windows 主机），无法获取时则回退到 `host.docker.internal`。如需手动指定，可通过环境变量覆盖：
			```bash
			export MYSQL_HOST=$(grep -m1 nameserver /etc/resolv.conf | awk '{print $2}')
			export MYSQL_PORT=3306
			export MYSQL_DATABASE=pet_shop
			export MYSQL_USER=root
			export MYSQL_PASSWORD=your_password
			uv run python manage.py runserver 0.0.0.0:8000
		```
	- 如果需要长期保存，可写入 `backstage/pet_shop/.env` 并在命令前追加 `UV_ENV_FILE=.env`.
3. **验证 WSL → Windows 连通性**
	- 可直接在 WSL 中测试：
			```bash
			mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -P "$MYSQL_PORT"
			```
		- 若连接失败，请检查 Windows MySQL 是否开放远程访问以及 IP/防火墙配置。

### AI 宠物顾问（LongCat API）

后台暴露了 `/ai/consult/` 接口来代理第三方 AI 能力，所有密钥仅在服务端配置：

```bash
export LONGCAT_API_KEY="在 LongCat 控制台获取的 key"
# 可选：覆盖默认模型或接口
export LONGCAT_MODEL="LongCat-Flash-Chat"
export LONGCAT_API_URL="https://api.longcat.chat/openai/v1/chat/completions"

UV_CACHE_DIR=/tmp/uv-cache uv run python manage.py runserver 0.0.0.0:8000
```

前端会调用 `http://localhost:8010/api/ai/consult/`，无须暴露真实 key。

### 商品预览限制

未登录用户只能浏览部分商品，登录后才能查看全部。可通过环境变量控制未登录时的可见数量：

```bash
export COMMODITY_PREVIEW_LIMIT=6  # 默认 6 条
```

### 收货地址与伪支付

- 后端基于 `backstage/pet_shop/data/china-regions.json` 内置的省市数据对收货地址进行校验，并通过 `/operation/regions/` 暴露级联数据，前端“用户中心”中的新增/编辑地址弹窗会强制选择合法的省市。
- `/trade/checkout/` 提供“伪支付”下单逻辑：前端在购物车中勾选商品、选择收货地址和支付方式后调用此接口即可生成订单，同时会清空已结算的购物车记录。

## 前端（Vue 3 + Vue CLI）

```bash
cd frontstage/pet_shop
npm install
npm run serve   # 默认端口 8080
```

前端默认与后端通过 `http://localhost:8010` / `http://localhost:8000` 等本地地址交互，如需修改请相应更新配置。

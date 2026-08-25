# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

吉祥宠物商城系统 (Lucky Pet Marketplace) — a full-stack e-commerce platform for pets. Vue 3 frontend, Django REST Framework backend, MySQL. Includes a customer storefront, a SimpleUI admin with an analytics dashboard, and an AI pet consultant backed by the LongCat API.

## Environment constraints (read first)

**Python 3.12 is required.** `pillow==10.3.0` does not build on 3.13, and `uv` will pick 3.13 by default. Always pass the pin:

```bash
uv sync --python 3.12
uv run --python 3.12 python manage.py <command>
```

**MySQL must be started manually on this machine.** `brew services start mysql` fails here with `Bootstrap failed: 5: Input/output error` from launchctl. Start it directly:

```bash
/opt/homebrew/opt/mysql/bin/mysqld_safe --datadir=/opt/homebrew/var/mysql &
```

The data directory was reinitialized on 2026-08-25 (a Homebrew protobuf upgrade broke the old MySQL 9.6 binary, and MySQL 26.7.0 refused to upgrade a 9.6 data dictionary). The previous datadir is preserved at `/opt/homebrew/var/mysql.old.960`. Schema comes from migrations; the superuser is `admin`.

`scripts/dev-up.sh` encodes all of the above.

## Development Commands

### Backend (`backstage/pet_shop/`)

```bash
cp .env.template .env                                          # first run only, then fill in
uv sync --python 3.12
uv run --python 3.12 python manage.py migrate
uv run --python 3.12 python manage.py seed_demo_business_data   # demo data for the dashboard
uv run --python 3.12 python manage.py runserver 127.0.0.1:8000
uv run --python 3.12 python manage.py test                     # 52 tests
uv run --python 3.12 python manage.py test trade.tests.CheckoutTests  # single class
```

### Frontend (`frontstage/pet_shop/`)

```bash
npm install
npm run serve    # port 8010, proxies /api -> http://127.0.0.1:8000
npm run build
npm run lint
```

## Configuration

All secrets and environment-specific values come from `backstage/pet_shop/.env`, which is gitignored. `.env.template` is committed and lists every variable with an explanation — treat it as the source of truth for configuration.

`settings.py` contains no secrets. `DJANGO_SECRET_KEY` is optional while `DJANGO_DEBUG=True` (an insecure dev fallback is used) and **required** when DEBUG is off — an unconfigured production boot raises `ImproperlyConfigured` rather than silently running with a known key.

## Architecture

### Backend apps

- **accounts** — `UserProfile` (FK to `auth.User`, not a OneToOne), registration, JWT login, captcha, avatar upload
- **commodity** — `CommodityInfos` (`sku_title`, `price`, `stock_quantity`, `sold`, `types`) and hierarchical `CommodityCategories`
- **trade** — `OrderInfos`, `OrderGoods`, `ShoppingCart`; CRUD in `views.py`, business actions (checkout / refund / confirm receipt / comment) in `api_views.py`
- **customer_operation** — addresses, favourites, messages, comments
- **merchant** — advertisements (read-only viewset)
- **charts** — analytics; `services.py` builds payloads, `views.py` exposes two `@staff_member_required` JSON endpoints
- **index** — AI pet consultant

Each app owns a `urls.py`, included from `pet_shop/urls.py` under `/api/`.

### Authentication

**JWT** (`djangorestframework-simplejwt`). `POST /api/accounts/login/` validates a captcha, then returns an `access`/`refresh` pair. The frontend stores only those two tokens and sends `Authorization: Bearer <access>`.

`src/api/index.js` holds the token helpers (`setAuthTokens`, `clearAuthTokens`, `getAccessToken`) and a response interceptor that transparently refreshes a 401 once via `/api/accounts/token/refresh/` and replays the request. Concurrent 401s share one in-flight refresh.

Captcha: `GET /api/accounts/captcha/?username=X` returns `{img}` only. The answer stays in Django's cache (60s TTL, key `verify_code_{username}`) and is deleted on first use, so a captcha cannot be replayed.

`SessionAuthentication` remains enabled for the DRF browsable API and the admin. CSRF middleware is **on** — do not disable it. An earlier `CsrfExemptSessionAuthentication` class existed purely to bypass CSRF and has been removed; don't reintroduce that pattern.

Ownership scoping lives in each ViewSet's `get_queryset()` (filtering on `request.user`), not in a global permission class. `IsOwnerOrReadOnly` depends on `obj.user`, so it must be declared per-view — putting it in `DEFAULT_PERMISSION_CLASSES` raises `AttributeError` on models without a `user` field. `trade/tests.py::CrossUserAccessTests` guards this.

### Analytics (`charts/`)

The cleanest code in the project; use it as the reference for style elsewhere.

- `constants.py` — business rules as named constants (which order statuses count toward GMV, refund bucket precedence, price bands, trend windows, low-stock threshold)
- `services.py` — pure payload builders (`build_overview_payload`, `build_dashboard_payload`), aggregating in the database rather than in Python, with a `_AnalyticsTimeContext` dataclass caching window bounds
- `views.py` — thin `@staff_member_required` wrappers
- `demo_seed.py` + `management/commands/seed_demo_business_data.py` — writes demo data into the real business tables, so the dashboard works without mock files

Every dashboard metric is scoped to the same rolling window. When adding one, thread `days` and `time_context` through — `_build_rating_summary` previously aggregated over all time and reported a lifetime average inside a "last 30 days" panel.

Admin charts render ECharts loaded from a CDN in the templates (`templates/admin/index.html`, `charts/templates/`). There is no Python charting library in the dependency set.

### Frontend

- `src/api/index.js` — every backend call as a named function on one axios instance; owns JWT storage and the refresh interceptor
- `src/axios/index.js` — a second, separate global axios instance used for cookie/CSRF flows; be aware both exist
- `src/store/` — Vuex with `vuex-persistedstate`
- `src/views/` pages, `src/components/` shared (Header/Footer registered globally in `main.js`)

## Testing

52 tests. Coverage is uneven by design of history: `charts/` was already well covered, and tests were added for the security fixes.

- `accounts/tests.py` — JWT login, captcha single-use and non-leakage
- `trade/tests.py` — cross-user access isolation, checkout stock/atomicity/`order_sn` uniqueness, rating bounds
- `index/tests.py` — AI endpoint auth, topic-filter whitelist precedence
- `charts/tests/` — analytics service, admin views, seed command, smoke test

Still untested: commodity and merchant views, serializers, the refund and confirm-receipt flows.

## Gotchas

- **`pet_shop_backup.sql` cannot be imported.** It is UTF-16LE encoded, its Chinese is already mojibake at rest, and line 48 has an unescaped quote making it a syntax error. Use `migrate` + `seed_demo_business_data`. The file is now gitignored (`*.sql`) because it contains real password hashes, emails and phone numbers.
- **Secrets remain in git history.** Untracking the dump and the 78 stale `.pyc` files stops future exposure but does not purge history. A real cleanup needs `git filter-repo`/BFG plus credential rotation — that decision is the maintainer's.
- **`LocMemCache` is per-process.** Captcha validation will fail intermittently under multiple workers. Set `CACHE_BACKEND`/`CACHE_LOCATION` to Redis for any multi-process deployment.
- **`.gitignore` excludes `media/` but 105 media files are tracked** (they predate the rule). Product images work, but newly added ones are silently ignored.
- **`order_status` semantics:** checkout sets `2` (发货中) directly, skipping `1` (已支付), because the refund and confirm-receipt flows gate on `order_status >= 2`. Changing it breaks those.
- **SimpleUI silently disables clickjacking protection.** `simpleui/apps.py` `ready()` pops `XFrameOptionsMiddleware` out of `MIDDLEWARE` unconditionally on Django 3+, with no opt-out, because its admin needs iframes. `X_FRAME_OPTIONS` therefore has no effect and `check --deploy` reports `security.W002`. The header has to be added at the reverse proxy for non-`/admin/` paths.
- Indentation is inconsistent: `charts/` uses 4 spaces, every other backend file uses tabs. Match the file you are editing.
- Model `verbose_name` values are Chinese and drive the SimpleUI admin labels.

## Conventions

- Python: snake_case, DRF ViewSets for CRUD, a separate `api_views.py` for non-CRUD business actions
- Frontend: 2-space indent, camelCase, Vue 3 Composition API, Element Plus
- Any multi-step write (order creation, stock movement) belongs in `transaction.atomic()` with `select_for_update()` on the contended rows — `CheckoutView` is the worked example

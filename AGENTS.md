# Repository Guidelines

## Project Structure & Module Organization

This is a full-stack pet marketplace system with separate frontend and backend directories:

- **Backend** (`backstage/pet_shop/`): Django REST API with MySQL database
  - `accounts/`: User authentication and profiles
  - `commodity/`: Product catalog and management
  - `trade/`: Order processing and payment handling
  - `customer_operation/`: Customer interactions and support
  - `merchant/`: Vendor management
  - `charts/`: Analytics and data visualization
  - `index/`: Homepage and landing content

- **Frontend** (`frontstage/pet_shop/`): Vue 3 application
  - `src/components/`: Reusable UI components
  - `src/views/`: Page-level components
  - `src/router/`: Vue Router configuration
  - `src/store/`: Vuex state management
  - `src/api/`: API service layer
  - `src/assets/`: Static assets and styles

## Build, Test, and Development Commands

### Backend (Django)

**Python 3.12 is required** — `pillow==10.3.0` does not build on 3.13, so every
`uv` invocation must pin the interpreter explicitly.

```bash
cd backstage/pet_shop
cp .env.template .env                                   # First run only; see Database Configuration
uv sync --python 3.12                                   # Install dependencies
uv run --python 3.12 python manage.py migrate            # Run database migrations
uv run --python 3.12 python manage.py runserver 127.0.0.1:8000  # Start development server
uv run --python 3.12 python manage.py test               # Run tests (52 currently pass)
uv run --python 3.12 python manage.py seed_demo_business_data   # Optional demo data (DEBUG=True only)
```

### Frontend (Vue 3)
```bash
cd frontstage/pet_shop
npm install                # Install dependencies
npm run serve              # Start development server (port 8010)
npm run build              # Build for production
npm run lint               # Run ESLint
```

## Coding Style & Naming Conventions

- **Backend**: Follow Django REST Framework patterns with 4-space indentation
- **Frontend**: Use Vue 3 Composition API with 2-space indentation
- **Naming**: Use snake_case for Python, camelCase for JavaScript
- **Formatting**: ESLint for frontend, no specific formatter for backend

## Testing Guidelines

- **Frontend**: ESLint configured with Vue 3 essential rules; no unit test setup
- **Backend**: Django's built-in testing framework. 52 tests pass today, almost
  all of them under `charts/tests/` (analytics service, seed command, admin
  views, seed-to-dashboard smoke test). Other apps' `tests.py` are mostly empty.
- **Coverage**: No specific coverage requirements defined
- **Test Naming**: Use descriptive test names that explain expected behavior

## Commit & Pull Request Guidelines

- **Commit Messages**: Use descriptive, present-tense messages
- **PR Requirements**: Include clear descriptions of changes and screenshots for UI updates
- **Issue Linking**: Reference related issues in PR descriptions
- **Code Review**: Ensure all tests pass before requesting review

## Database Configuration

- MySQL 8.0+, reached at `127.0.0.1:3306` by default on this checkout
- All settings come from `backstage/pet_shop/.env`, which is gitignored. Copy it
  from the committed `.env.template`, which lists every supported variable.
  `settings.py` contains no SECRET_KEY and no DB password.
  - `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
  - `DJANGO_SECRET_KEY` is **required** when `DJANGO_DEBUG=False`; the app
    refuses to boot without it. With DEBUG on, an insecure dev fallback is used.
- When `MYSQL_HOST` is unset, `settings.detect_mysql_host()` probes the
  environment: under WSL2 it reads the first nameserver from `/etc/resolv.conf`
  (which points at the Windows host), otherwise it uses `127.0.0.1`. Setting
  `MYSQL_HOST` in `.env` bypasses the probe entirely — that is the normal path.
- Database migrations managed via Django's migration system
- `pet_shop_backup.sql` is no longer tracked (`*.sql` is gitignored) and it
  **cannot be imported**: UTF-16LE encoded, mojibake Chinese, and one unescaped
  quote. The supported way to get data is `migrate` followed by
  `seed_demo_business_data`.
- Cache defaults to `LocMemCache`, not Redis. It is per-process, and captcha
  answers live in it, so multi-worker deployments need Redis via
  `CACHE_BACKEND` / `CACHE_LOCATION` or captcha validation breaks.

## Authentication

- Frontend auth is **JWT** (`djangorestframework-simplejwt`).
  `POST /api/accounts/login/` takes `{username, password, code}` and returns
  `access` / `refresh` alongside the user fields.
- The `code` is a captcha: `GET /api/accounts/captcha/?username=X` returns only
  `{img}` (base64 JPEG). The answer stays in the Django cache for 60s and is
  single-use.
- Clients store only `access_token` / `refresh_token` and send
  `Authorization: Bearer <access>`. Refresh via
  `POST /api/accounts/token/refresh/`; verify via `token/verify/`.
- The logout route is `/api/accounts/loginout/`, **not** `/logout/`.
- CSRF middleware is enabled and CORS uses an explicit allowlist
  (`CORS_ALLOWED_ORIGINS`) — no wildcard origins.

## AI Integration

- LongCat AI API integration for pet consultation features
- API keys configured via `LONGCAT_API_KEY` environment variable; without it the
  endpoint returns 503
- AI endpoint exposed at `/api/ai/consult/`. It **requires authentication** and
  is rate limited (`THROTTLE_AI_CONSULT`, default 10/min)
- Model, `max_tokens`, and `temperature` are fixed server-side; request-body
  overrides are ignored. Messages are capped at 2000 chars each

## Environment Setup

- Backend uses `uv` for Python dependency management, pinned to Python 3.12
- Frontend uses npm with Vite (`vite.config.js`; migrated from Vue CLI/webpack)
- Development servers run on 127.0.0.1:8000 (backend) and 8010 (frontend);
  `vite.config.js` proxies `/api` to `http://127.0.0.1:8000`
- Frontend env vars use the `VITE_*` prefix (`VITE_API_BASE_URL`), read via
  `import.meta.env`; the old `VUE_APP_*` names no longer exist
- Cross-origin requests handled by django-cors-headers against an explicit
  allowlist that must include the frontend origin
- Admin charts load ECharts from a jsDelivr CDN in `templates/admin/index.html`;
  there is no Python charting library in the dependency set

## Agent-Specific Instructions

- When modifying backend code, ensure database migrations are created if models change
- Always pass `--python 3.12` to `uv sync` / `uv run`
- Frontend API calls should go through `src/api/index.js`, which owns the JWT
  interceptor and the automatic refresh-and-replay on 401
- AI features require proper API key configuration and a logged-in user
- Verify model field names against the models rather than assuming them — e.g.
  `CommodityInfos` uses `sku_title`, `price`, `stock_quantity`, `sold`, `types`

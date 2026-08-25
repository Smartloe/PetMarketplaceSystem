#!/usr/bin/env bash
# Local dev startup for 吉祥宠物商城系统 (Pet Marketplace System)
# Usage: ./scripts/dev-up.sh
#
# Encodes three machine-specific constraints:
#   1. Python 3.12 is required — pillow==10.3.0 does not build on 3.13,
#      and uv would otherwise pick 3.13.
#   2. `brew services start mysql` fails on this host with a launchctl
#      I/O error, so MySQL is started via mysqld_safe directly.
#   3. Backend config comes from backstage/pet_shop/.env (gitignored).
#      Copy it from .env.template on first run.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BE="$ROOT/backstage/pet_shop"
FE="$ROOT/frontstage/pet_shop"
PY=3.12

if [ ! -f "$BE/.env" ]; then
  echo "==> No .env found. Creating one from .env.template..."
  cp "$BE/.env.template" "$BE/.env"
  echo "    Edit $BE/.env and set MYSQL_PASSWORD before continuing."
  exit 1
fi

# shellcheck disable=SC1091
MYSQL_PASS="$(grep -E '^MYSQL_PASSWORD=' "$BE/.env" | cut -d= -f2-)"

echo "==> Ensuring MySQL is running..."
if ! mysqladmin -u root -p"$MYSQL_PASS" ping >/dev/null 2>&1; then
  echo "    Not responding; starting mysqld_safe (launchctl path is broken on this host)..."
  /opt/homebrew/opt/mysql/bin/mysqld_safe --datadir=/opt/homebrew/var/mysql &
  for _ in $(seq 1 20); do
    if mysqladmin -u root -p"$MYSQL_PASS" ping >/dev/null 2>&1; then break; fi
    sleep 1
  done
fi
echo "    MySQL up."

echo "==> Backend deps (Python $PY)..."
( cd "$BE" && uv sync --python "$PY" )

echo "==> Migrations..."
( cd "$BE" && uv run --python "$PY" python manage.py migrate )

echo "==> Frontend deps..."
( cd "$FE" && npm install )

echo "==> Starting backend (:8000) and frontend (:8010). Ctrl-C stops both."
trap 'kill 0' EXIT
( cd "$BE" && uv run --python "$PY" python manage.py runserver 127.0.0.1:8000 ) &
( cd "$FE" && npm run serve ) &
wait

#!/bin/sh
set -e

echo "→ Entrypoint start (PORT=${PORT:-8000})"

wait_for_db() {
  python <<'PY'
import os
import sys
import time

url = os.environ.get("DATABASE_URL", "")
if not url or url.startswith("sqlite"):
    print("→ No Postgres DATABASE_URL; skipping wait")
    sys.exit(0)

import dj_database_url

cfg = dj_database_url.parse(url)
engine = cfg.get("ENGINE", "")
if "postgresql" not in engine and "postgres" not in engine:
    sys.exit(0)

import psycopg

host = cfg.get("HOST") or "localhost"
port = int(cfg.get("PORT") or 5432)
name = cfg.get("NAME")
user = cfg.get("USER")
password = cfg.get("PASSWORD")

print(f"→ Waiting for PostgreSQL at {host}:{port}/{name} ...")
print(f"→ DB user={user!r} name={name!r}")
for attempt in range(1, 61):
    try:
        with psycopg.connect(
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password,
            connect_timeout=3,
        ) as conn:
            conn.execute("SELECT 1")
        print("→ PostgreSQL ready")
        sys.exit(0)
    except Exception as exc:
        print(f"  attempt {attempt}/60: {exc}")
        time.sleep(2)

print("PostgreSQL unavailable", file=sys.stderr)
sys.exit(1)
PY
}

wait_for_db

echo "→ makemigrations..."
python manage.py makemigrations --noinput || {
  echo "⚠ makemigrations uyarı/hata verdi, migrate ile devam"
}

echo "→ migrate..."
python manage.py migrate --noinput

echo "→ collectstatic..."
python manage.py collectstatic --noinput || true

if [ "${SEED_PROJECTS:-False}" = "True" ] || [ "${SEED_PROJECTS:-false}" = "true" ]; then
  echo "→ Seeding products..."
  python manage.py seed_projects || true
fi

if [ "${SEED_MENUS:-True}" = "True" ] || [ "${SEED_MENUS:-true}" = "true" ]; then
  echo "→ Seeding menus..."
  python manage.py seed_menus || true
  echo "→ Seeding footer..."
  python manage.py seed_footer || true
fi

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "→ Ensuring superuser exists..."
  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email = os.environ["DJANGO_SUPERUSER_EMAIL"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
user, created = User.objects.get_or_create(username=username, defaults={"email": email})
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print("created" if created else "updated", username)
PY
fi

echo "→ Django check..."
python manage.py check || true

echo "→ Starting: $*"
exec "$@"

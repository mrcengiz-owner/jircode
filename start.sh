#!/bin/sh
set -e

PORT="${PORT:-8000}"
echo "→ JîrCode start (PORT=${PORT})"

# --- Postgres bekle ---
python <<'PY'
import os, sys, time
url = os.environ.get("DATABASE_URL", "")
if not url or url.startswith("sqlite"):
    print("→ SQLite / no DATABASE_URL")
    sys.exit(0)
import dj_database_url, psycopg
cfg = dj_database_url.parse(url)
if "postgres" not in cfg.get("ENGINE", ""):
    sys.exit(0)
host, port = cfg.get("HOST") or "localhost", int(cfg.get("PORT") or 5432)
name, user, password = cfg.get("NAME"), cfg.get("USER"), cfg.get("PASSWORD")
print(f"→ Waiting Postgres {host}:{port}/{name} user={user}")
for i in range(1, 61):
    try:
        with psycopg.connect(host=host, port=port, dbname=name, user=user, password=password, connect_timeout=3) as c:
            c.execute("SELECT 1")
        print("→ PostgreSQL ready")
        sys.exit(0)
    except Exception as e:
        print(f"  {i}/60: {e}")
        time.sleep(2)
print("PostgreSQL unavailable", file=sys.stderr)
sys.exit(1)
PY

echo "→ makemigrations"
python manage.py makemigrations --noinput || true

echo "→ migrate"
python manage.py migrate --noinput

echo "→ collectstatic"
python manage.py collectstatic --noinput || true

if [ "${SEED_PROJECTS:-True}" = "True" ] || [ "${SEED_PROJECTS:-true}" = "true" ]; then
  python manage.py seed_projects || true
fi
if [ "${SEED_MENUS:-True}" = "True" ] || [ "${SEED_MENUS:-true}" = "true" ]; then
  python manage.py seed_menus || true
  python manage.py seed_footer || true
fi

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
U = get_user_model()
u, created = U.objects.get_or_create(
    username=os.environ["DJANGO_SUPERUSER_USERNAME"],
    defaults={"email": os.environ.get("DJANGO_SUPERUSER_EMAIL", "")},
)
u.email = os.environ.get("DJANGO_SUPERUSER_EMAIL", u.email)
u.is_staff = True
u.is_superuser = True
u.set_password(os.environ["DJANGO_SUPERUSER_PASSWORD"])
u.save()
print("superuser", "created" if created else "updated")
PY
fi

echo "→ Gunicorn 0.0.0.0:${PORT}"
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers 3 \
  --threads 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -

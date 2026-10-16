#!/sh
set -e

echo "→ Running migrations..."
python manage.py migrate --noinput

if [ "${SEED_PROJECTS:-False}" = "True" ] || [ "${SEED_PROJECTS:-false}" = "true" ]; then
  echo "→ Seeding sample projects..."
  python manage.py seed_projects
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

echo "→ Starting: $*"
exec "$@"

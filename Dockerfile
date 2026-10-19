FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Build-time collectstatic (SECRET_KEY sadece build için)
ENV SECRET_KEY=build-only-not-for-production \
    DEBUG=False \
    ALLOWED_HOSTS=*

RUN sed -i 's/\r$//' /app/start.sh /app/entrypoint.sh \
    && chmod +x /app/start.sh /app/entrypoint.sh \
    && mkdir -p /app/media /app/staticfiles \
    && python manage.py collectstatic --noinput

EXPOSE 8000

# Dokploy Application: tek CMD — ENTRYPOINT yok (Dokploy override bozmasın)
# Panelde Port = 8000, Domain Port = 8000
# Host header zorunlu (DisallowedHost 400 → unhealthy → Traefik 502)
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=5 \
  CMD curl -fsS -H "Host: localhost" "http://127.0.0.1:${PORT:-8000}/healthz/" || exit 1

CMD ["/bin/sh", "/app/start.sh"]

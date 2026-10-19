# Dokploy — Application (Dockerfile)

Compose kullanma. Uygulama tipi: **Application**.

## Kurulum

1. **Application** oluştur → Provider: **Dockerfile**
2. Dockerfile: `Dockerfile` (kök dizin)
3. Port: **8000** (Domains portu da **8000** olmalı)
4. **Command / Args boş bırak** — start `CMD ["/bin/sh", "/app/start.sh"]`
5. Environment variables yapıştır
6. Domains:
   - `www.jircode.com` → port `8000` → HTTPS
   - `jircode.com` → port `8000` → HTTPS
7. Volume (opsiyonel): `/app/media`
8. Deploy

Her deploy’da (`start.sh`) otomatik:
- Postgres bekle → `makemigrations` → `migrate` → `collectstatic`
- seed (menü/ürün/footer) + superuser → Gunicorn `:8000`

## 502 Bad Gateway

Traefik domain’i buluyor ama container cevap vermiyor.

Kontrol:
1. Application **Logs** (build değil): `→ Gunicorn` / `Listening at: http://0.0.0.0:8000`
2. `PostgreSQL unavailable` → `DATABASE_URL` host/şifre (`%2E`)
3. Domain port = uygulama port = `8000`
4. Custom Command doluysa silip yeniden deploy
5. Cloudflare SSL = **Full**

## Notlar

- Postgres host: `postgres-postgres-tjksoo` (Dokploy internal)
- Şifredeki `.` URL'de `%2E` olmalı
- Cloudflare apex→www redirect ayrıca kalabilir

# Dokploy — Application (Dockerfile)

Compose kullanma. Uygulama tipi: **Application**.

## Kurulum

1. **Application** oluştur → Provider: **Dockerfile**
2. Dockerfile: `Dockerfile` (kök dizin)
3. Port: **8000** (Domains portu da **8000** olmalı)
4. Environment variables yapıştır
5. Domains:
   - `www.jircode.com` → port `8000` → HTTPS
   - `jircode.com` → port `8000` → HTTPS
6. Volume (opsiyonel): `/app/media`
7. Deploy

Her deploy’da otomatik:
- `makemigrations`
- `migrate`
- `collectstatic`
- seed (menü/ürün/footer) + superuser

## 502 Bad Gateway

Traefik domain’i buluyor ama container cevap vermiyor.

Kontrol:
1. Logs’ta `Listening at: http://0.0.0.0:8000` var mı?
2. `PostgreSQL unavailable` varsa `DATABASE_URL` yanlış
3. Domain port = uygulama port = `8000`
4. Cloudflare SSL = **Full** (seçili)

## Notlar

- Postgres host: `postgres-postgres-tjksoo` (Dokploy internal)
- Şifredeki `.` URL'de `%2E` olmalı
- Cloudflare apex→www redirect ayrıca kalabilir

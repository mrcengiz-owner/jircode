# Dokploy — Application (Dockerfile)

Compose kullanma. Uygulama tipi: **Application**.

## Kurulum

1. **Application** oluştur → Provider: **Dockerfile**
2. Dockerfile: `Dockerfile` (kök dizin)
3. Port: **8000**
4. Environment variables: aşağıdaki env bloğunu yapıştır
5. Domains:
   - `www.jircode.com` → port `8000` → HTTPS
   - `jircode.com` → port `8000` → HTTPS
6. Volume (opsiyonel): `/app/media`
7. Deploy

## Notlar

- Postgres host: `postgres-postgres-tjksoo` (Dokploy internal)
- Şifredeki `.` URL'de `%2E` olmalı
- Cloudflare apex→www redirect ayrıca kalabilir

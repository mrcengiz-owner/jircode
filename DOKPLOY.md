# Dokploy 404 düzeltmesi

## Kritik adım (Preview’daki label çakışması)

Dokploy Domains’in ürettiği label’lar her domain için **ayrı Traefik service** açıyor
(`...-8-websecure`, `...-9-websecure`). Bu yapıda origin sıkça `404 page not found` döner.

### Yapılacaklar

1. Dokploy uygulama → **Domains**
2. `jircode.com` ve `www.jircode.com` domain kayıtlarını **SİL**
3. Bu repo’daki `docker-compose.yml` push edilmiş olsun
4. **Redeploy**
5. Preview Compose’ta sadece şunlar görünsün:
   - `traefik.http.services.jircode-web.loadbalancer.server.port=8000`
   - `Host(\`www.jircode.com\`) || Host(\`jircode.com\`)`
   - `...-8-websecure` / `...-9-websecure` **olmasın**
6. Logs: `Listening at: http://0.0.0.0:8000`

## Env

```env
DATABASE_URL=postgresql://mrcengiz:Murat1993%2E@postgres-postgres-tjksoo:5432/jircode
```

(Şifredeki `.` → `%2E`)

## Cloudflare

DNS doğru. Apex→www redirect ayrı konu; 404 Traefik route kaynaklı.

# Dokploy — 404 çözümü (jircode.com)

DNS ve Cloudflare doğru. Origin Traefik `404 page not found` veriyor =
**container Traefik’e bağlı değil veya çalışmıyor.**

## A) Compose ile (mevcut)

1. Push + **Redeploy**
2. **Deployments / Logs**
   - `web` durumu: **Running** (Restarting olmasın)
   - Logda: `Listening at: http://0.0.0.0:8000`
3. **Domains** (ikisi de):
   - `www.jircode.com` → Service **`web`** → Port **`8000`** → HTTPS
   - `jircode.com` → Service **`web`** → Port **`8000`** → HTTPS
4. Domain değişince tekrar **Redeploy**
5. **Preview Compose** içinde şunlar olmalı:
   - `networks: dokploy-network`
   - `Host(\`www.jircode.com\`)`
   - `loadbalancer.server.port=8000`
   - Manuel ekstra `traefik.http.routers.jircode...` **olmamalı**

## B) Daha stabil: Application (Dockerfile)

Compose sorun çıkarıyorsa:

1. Yeni uygulama tipi: **Application** → **Dockerfile**
2. Dockerfile path: `Dockerfile`
3. Port: `8000`
4. Aynı env değişkenlerini yapıştır
5. Domains: `www.jircode.com` + `jircode.com` → port `8000`
6. Deploy

## DATABASE_URL

Şifrede nokta varsa encoded kullan:

```env
DATABASE_URL=postgresql://mrcengiz:Murat1993%2E@postgres-postgres-tjksoo:5432/jircode
```

## Cloudflare

- DNS A kayıtları `31.77.112.220` + Proxied → doğru
- Apex → www redirect kuralı → doğru (ayrı konu)
- 404’ün kaynağı Cloudflare değil, Dokploy/Traefik

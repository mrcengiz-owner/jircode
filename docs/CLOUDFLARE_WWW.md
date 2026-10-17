# jircode.com → www.jircode.com (Cloudflare)

DNS Cloudflare’de. Apex (`jircode.com`) şu an origin’e gidiyor ama
Dokploy/Traefik’te yalnızca `www` route’u olduğu için **404** dönüyor.

En temiz çözüm: Cloudflare’de apex’i www’ye yönlendirmek.

## Redirect Rule (önerilen)

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → **jircode.com**
2. **Rules** → **Redirect Rules** → **Create rule**
3. Ayarlar:

| Alan | Değer |
|---|---|
| Rule name | `Apex to www` |
| When incoming requests match | Custom filter expression |
| Expression | `(http.host eq "jircode.com")` |
| Then | Dynamic |
| Expression | `concat("https://www.jircode.com", http.request.uri.path)` |
| Status code | `301` |
| Preserve query string | Açık |

4. **Deploy**

Bundan sonra `https://jircode.com/...` otomatik `https://www.jircode.com/...` olur.

## DNS kontrol

- `jircode.com` → Proxied (turuncu bulut) A/AAAA veya CNAME
- `www` → Proxied, aynı origin’e

SSL/TLS modu genelde **Full** veya **Full (strict)** olmalı.

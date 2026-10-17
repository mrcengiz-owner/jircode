from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """
    CANONICAL_HOST=www.jircode.com ise diğer host'ları oraya 301 ile yönlendirir.
    Dokploy'da hem apex hem www domain bağlı olmalı; aksi halde istek uygulamaya gelmez.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical = (getattr(settings, "CANONICAL_HOST", "") or "").strip().lower()

    def __call__(self, request):
        if self.canonical:
            host = request.get_host().split(":")[0].lower()
            if host and host != self.canonical:
                return HttpResponsePermanentRedirect(
                    f"{request.scheme}://{self.canonical}{request.get_full_path()}"
                )
        return self.get_response(request)

from django.conf import settings


def site_defaults(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_EMAIL": settings.SITE_EMAIL,
        "SITE_LOCATION": settings.SITE_LOCATION,
    }

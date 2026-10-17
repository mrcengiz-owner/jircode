from django.conf import settings

from .models import MenuItem


def site_defaults(request):
    current = getattr(request.resolver_match, "url_name", None)
    menu_qs = MenuItem.objects.filter(is_active=True)

    header_menu = []
    for item in menu_qs.filter(location=MenuItem.LOCATION_HEADER):
        item.is_current_page = item.is_current(current)
        header_menu.append(item)

    footer_menu = list(menu_qs.filter(location=MenuItem.LOCATION_FOOTER))

    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_EMAIL": settings.SITE_EMAIL,
        "SITE_LOCATION": settings.SITE_LOCATION,
        "header_menu": header_menu,
        "footer_menu": footer_menu,
        "current_url_name": current,
    }

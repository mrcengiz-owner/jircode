from django.core.management.base import BaseCommand

from core.models import MenuItem


DEFAULT_ITEMS = [
    {
        "title": "Ana Sayfa",
        "location": MenuItem.LOCATION_HEADER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "home",
        "sort_order": 1,
    },
    {
        "title": "Hakkımızda",
        "location": MenuItem.LOCATION_HEADER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "about",
        "sort_order": 2,
    },
    {
        "title": "Hizmetler",
        "location": MenuItem.LOCATION_HEADER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "services",
        "sort_order": 3,
    },
    {
        "title": "Ürünler",
        "location": MenuItem.LOCATION_HEADER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "projects",
        "match_names": "projects,project_detail",
        "sort_order": 4,
    },
    {
        "title": "İletişim",
        "location": MenuItem.LOCATION_HEADER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "contact",
        "is_button": True,
        "sort_order": 5,
    },
    {
        "title": "Hakkımızda",
        "location": MenuItem.LOCATION_FOOTER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "about",
        "sort_order": 1,
    },
    {
        "title": "Hizmetler",
        "location": MenuItem.LOCATION_FOOTER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "services",
        "sort_order": 2,
    },
    {
        "title": "Ürünler",
        "location": MenuItem.LOCATION_FOOTER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "projects",
        "sort_order": 3,
    },
    {
        "title": "İletişim formu",
        "location": MenuItem.LOCATION_FOOTER,
        "link_type": MenuItem.LINK_INTERNAL,
        "url_name": "contact",
        "sort_order": 4,
    },
]


class Command(BaseCommand):
    help = "Varsayılan menü öğelerini ekler (eksik olanlar)."

    def handle(self, *args, **options):
        created = 0
        for item in DEFAULT_ITEMS:
            defaults = {
                "link_type": item["link_type"],
                "url_name": item.get("url_name", ""),
                "custom_url": item.get("custom_url", ""),
                "match_names": item.get("match_names", ""),
                "is_button": item.get("is_button", False),
                "is_active": True,
                "sort_order": item["sort_order"],
                "open_in_new_tab": item.get("open_in_new_tab", False),
            }
            obj, was_created = MenuItem.objects.get_or_create(
                title=item["title"],
                location=item["location"],
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                # Sıra/aktiflik korunur; sadece boş alanları doldurma
                updated = False
                for key, value in defaults.items():
                    if key in ("sort_order", "is_active", "is_button"):
                        continue
                    if not getattr(obj, key) and value:
                        setattr(obj, key, value)
                        updated = True
                if updated:
                    obj.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Menü seed: {created} yeni, toplam {MenuItem.objects.count()} öğe."
            )
        )

from django.core.management.base import BaseCommand

from core.models import FooterSettings


class Command(BaseCommand):
    help = "Varsayılan footer ayarlarını oluşturur."

    def handle(self, *args, **options):
        footer = FooterSettings.load()
        self.stdout.write(self.style.SUCCESS(f"Footer hazır: {footer}"))

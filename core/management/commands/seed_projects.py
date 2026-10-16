from django.core.management.base import BaseCommand

from core.models import Project


PRODUCTS = [
    {
        "title": "JîrCode Mail",
        "slug": "jircode-mail",
        "summary": "Gizlilik odaklı, kendi sunucunuzda çalışan kurumsal e-posta platformu.",
        "description": (
            "JîrCode Mail, işletmelerin e-posta altyapısını dış SaaS bağımlılığı olmadan "
            "yönetmesi için geliştirilmiş privacy-first bir self-hosted mail platformudur.\n\n"
            "Kurumsal hesap yönetimi, güvenli giriş ve sade bir yönetim deneyimi sunar. "
            "Verileriniz sizin kontrolünüzde kalır; iletişim altyapınız markanızın parçası olur.\n\n"
            "Öne çıkanlar:\n"
            "• Self-hosted kurumsal e-posta\n"
            "• Gizlilik odaklı mimari\n"
            "• Kurulum ve hesap yönetimi\n"
            "• JîrCode ekosistemiyle uyumlu yapı\n\n"
            "Canlı ürün: https://mail.jircode.com"
        ),
        "tech_stack": "Self-hosted Mail, Privacy, Kurumsal E-posta",
        "project_url": "https://mail.jircode.com",
        "is_featured": True,
        "is_published": True,
        "sort_order": 1,
    },
    {
        "title": "JîrChat",
        "slug": "jircode-chat",
        "summary": "Kanallar, dosyalar ve aramalar — kendi sunucunuzda kurumsal anlık mesajlaşma.",
        "description": (
            "JîrChat, JîrCode’un kurumsal anlık mesajlaşma ürünüdür. "
            "Ekip kanalları, özel yazışmalar, dosya paylaşımı ve aramalar aynı oturumda yürür; "
            "yönetim kendi altyapınızda kalır.\n\n"
            "İletişim tek yerde, kontrol sizde. Veri sizin sunucunuzda tutulur; "
            "roller erişimi sınırlar, gerektiğinde uçtan uca şifreleme açılır.\n\n"
            "Öne çıkanlar:\n"
            "• Kanallar ve doğrudan mesajlar\n"
            "• Dosya / medya paylaşımı ve önizleme\n"
            "• WebRTC ses-görüntü aramaları ve ekran paylaşımı\n"
            "• On-premise veya private cloud kurulum\n"
            "• Web, Windows ve Linux istemcileri\n\n"
            "Canlı ürün: https://chat.jircode.com"
        ),
        "tech_stack": "Anlık Mesajlaşma, WebRTC, Self-hosted, E2EE",
        "project_url": "https://chat.jircode.com",
        "is_featured": True,
        "is_published": True,
        "sort_order": 2,
    },
    {
        "title": "Açık Masa",
        "slug": "acik-masa",
        "summary": "Restoran ve kafeler için QR’lı dijital menü platformu.",
        "description": (
            "Açık Masa, restoran ve kafelerin menüsünü fotoğraflı, kalori detaylı ve "
            "markaya özel bir deneyimle misafire ulaştıran dijital menü platformudur.\n\n"
            "İşletmeniz nordkafe.acikmasa.net gibi özel bir subdomain ile yayına çıkar. "
            "Misafir QR’ı tarar, menüye girer; siz panelden anında güncellersiniz. "
            "Uygulama indirmeye gerek yoktur.\n\n"
            "Öne çıkanlar:\n"
            "• Özel subdomain ile anında yayın\n"
            "• QR ile sürtünmesiz erişim\n"
            "• Ürün fotoğrafı, kalori ve alerjen bilgisi\n"
            "• Kategori sekmeleri ve detay popup sunumu\n"
            "• Başlangıç, Profesyonel ve İşletme paketleri\n\n"
            "Canlı ürün: https://acikmasa.net"
        ),
        "tech_stack": "Dijital Menü, QR, SaaS, Restoran Teknolojisi",
        "project_url": "https://acikmasa.net",
        "is_featured": True,
        "is_published": True,
        "sort_order": 3,
    },
]

LEGACY_SLUGS = ("mesohq", "jircode-corporate", "sentinel-agent")


class Command(BaseCommand):
    help = "JîrCode ürünlerini ekler/günceller (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for item in PRODUCTS:
            _, was_created = Project.objects.update_or_create(
                slug=item["slug"],
                defaults=item,
            )
            if was_created:
                created += 1

        unpublished = Project.objects.filter(slug__in=LEGACY_SLUGS).update(
            is_published=False,
            is_featured=False,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed tamam: {created} yeni, {len(PRODUCTS)} ürün güncel, "
                f"{unpublished} eski kayıt yayından alındı."
            )
        )

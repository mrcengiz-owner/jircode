from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.text import slugify


class MenuItem(models.Model):
    LOCATION_HEADER = "header"
    LOCATION_FOOTER = "footer"
    LOCATION_CHOICES = [
        (LOCATION_HEADER, "Üst menü"),
        (LOCATION_FOOTER, "Alt menü"),
    ]

    LINK_INTERNAL = "internal"
    LINK_EXTERNAL = "external"
    LINK_CHOICES = [
        (LINK_INTERNAL, "İç sayfa (URL adı)"),
        (LINK_EXTERNAL, "Özel / dış link"),
    ]

    URL_NAME_CHOICES = [
        ("home", "Ana Sayfa"),
        ("about", "Hakkımızda"),
        ("services", "Hizmetler"),
        ("projects", "Ürünler"),
        ("contact", "İletişim"),
    ]

    title = models.CharField("Başlık", max_length=80)
    location = models.CharField(
        "Konum",
        max_length=20,
        choices=LOCATION_CHOICES,
        default=LOCATION_HEADER,
        db_index=True,
    )
    link_type = models.CharField(
        "Link tipi",
        max_length=20,
        choices=LINK_CHOICES,
        default=LINK_INTERNAL,
    )
    url_name = models.CharField(
        "İç sayfa",
        max_length=64,
        blank=True,
        choices=URL_NAME_CHOICES,
        help_text="İç sayfa seçerseniz otomatik route kullanılır.",
    )
    custom_url = models.CharField(
        "Özel URL",
        max_length=300,
        blank=True,
        help_text="Örn: /projeler/ veya https://mail.jircode.com",
    )
    open_in_new_tab = models.BooleanField("Yeni sekmede aç", default=False)
    is_button = models.BooleanField(
        "Buton görünümü",
        default=False,
        help_text="Üst menüde CTA butonu olarak gösterilir.",
    )
    match_names = models.CharField(
        "Aktif sayfa eşleşmesi",
        max_length=200,
        blank=True,
        help_text="Virgülle URL adları. Örn: projects,project_detail",
    )
    is_active = models.BooleanField("Aktif", default=True)
    sort_order = models.PositiveIntegerField("Sıra", default=0)

    class Meta:
        ordering = ["location", "sort_order", "id"]
        verbose_name = "Menü öğesi"
        verbose_name_plural = "Menü öğeleri"

    def __str__(self):
        return f"{self.get_location_display()} — {self.title}"

    def get_href(self):
        if self.link_type == self.LINK_INTERNAL and self.url_name:
            try:
                return reverse(self.url_name)
            except NoReverseMatch:
                return self.custom_url or "#"
        return self.custom_url or "#"

    def is_current(self, url_name: str | None) -> bool:
        if not url_name:
            return False
        names = {n.strip() for n in self.match_names.split(",") if n.strip()}
        if self.url_name:
            names.add(self.url_name)
        return url_name in names


class Project(models.Model):
    title = models.CharField("Başlık", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField("Kısa özet", max_length=280)
    description = models.TextField("Açıklama")
    tech_stack = models.CharField(
        "Teknolojiler",
        max_length=300,
        help_text="Virgülle ayırın: Django, PostgreSQL, React",
        blank=True,
    )
    project_url = models.URLField("Proje linki", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    cover = models.ImageField("Kapak görseli", upload_to="projects/", blank=True)
    is_featured = models.BooleanField("Öne çıkan", default=False)
    is_published = models.BooleanField("Yayında", default=True)
    sort_order = models.PositiveIntegerField("Sıra", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "proje"
            slug = base
            n = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})

    def tech_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class ContactMessage(models.Model):
    name = models.CharField("Ad Soyad", max_length=120)
    email = models.EmailField("E-posta")
    subject = models.CharField("Konu", max_length=200)
    message = models.TextField("Mesaj")
    is_read = models.BooleanField("Okundu", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "İletişim mesajı"
        verbose_name_plural = "İletişim mesajları"

    def __str__(self):
        return f"{self.name} — {self.subject}"


class WaitlistEntry(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bekleme listesi"
        verbose_name_plural = "Bekleme listesi"

    def __str__(self):
        return self.email

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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

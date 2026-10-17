from django.contrib import admin

from .models import ContactMessage, MenuItem, Project, WaitlistEntry


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "location",
        "link_type",
        "url_name",
        "custom_url",
        "is_button",
        "is_active",
        "sort_order",
    )
    list_filter = ("location", "link_type", "is_active", "is_button")
    search_fields = ("title", "custom_url", "url_name")
    list_editable = ("is_active", "is_button", "sort_order")
    ordering = ("location", "sort_order", "id")
    fieldsets = (
        (None, {"fields": ("title", "location", "sort_order", "is_active")}),
        (
            "Bağlantı",
            {
                "fields": (
                    "link_type",
                    "url_name",
                    "custom_url",
                    "open_in_new_tab",
                    "match_names",
                )
            },
        ),
        ("Görünüm", {"fields": ("is_button",)}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_published", "sort_order", "updated_at")
    list_filter = ("is_featured", "is_published")
    search_fields = ("title", "summary", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "is_published", "sort_order")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)

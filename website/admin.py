from django.contrib import admin
from .models import (
    AboutPage,
    AboutTimelineItem,
    ContactPage,
    ContactSubmission,
    HomeFeature,
    HomePage,
)


class SingletonPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class HomeFeatureInline(admin.TabularInline):
    model = HomeFeature
    extra = 1
    fields = ("title", "description", "order", "is_active")


@admin.register(HomePage)
class HomePageAdmin(SingletonPageAdmin):
    inlines = [HomeFeatureInline]
    fieldsets = (
        ("Hero Section", {
            "fields": (
                "hero_eyebrow",
                "hero_title",
                "hero_description",
                "primary_button_label",
                "secondary_button_label",
            )
        }),
        ("Company Introduction", {
            "fields": ("intro_eyebrow", "intro_title")
        }),
        ("Dynamic Catalog Sections", {
            "fields": (
                "brands_eyebrow",
                "brands_title",
                "categories_eyebrow",
                "categories_title",
            )
        }),
        ("CTA Section", {
            "fields": ("cta_eyebrow", "cta_title", "cta_button_label")
        }),
    )


class AboutTimelineItemInline(admin.TabularInline):
    model = AboutTimelineItem
    extra = 1
    fields = ("title", "description", "order", "is_active")


@admin.register(AboutPage)
class AboutPageAdmin(SingletonPageAdmin):
    inlines = [AboutTimelineItemInline]
    fieldsets = (
        ("Company Overview", {
            "fields": ("eyebrow", "title", "overview")
        }),
        ("Mission and Vision", {
            "fields": ("mission_title", "mission_text", "vision_title", "vision_text")
        }),
        ("Operations Sections", {
            "fields": (
                "warehouse_title",
                "warehouse_text",
                "network_title",
                "network_text",
                "why_title",
                "why_text",
            )
        }),
        ("Brands and Timeline", {
            "fields": (
                "brands_eyebrow",
                "brands_title",
                "timeline_eyebrow",
                "timeline_title",
            )
        }),
    )


@admin.register(ContactPage)
class ContactPageAdmin(SingletonPageAdmin):
    fieldsets = (
        ("Page Header", {
            "fields": ("eyebrow", "title", "description")
        }),
        ("Contact Information", {
            "fields": (
                "address_label",
                "address",
                "email_label",
                "email",
                "phone_label",
                "phone",
            )
        }),
        ("Map and Form", {
            "fields": (
                "map_title",
                "map_description",
                "google_maps_embed_url",
                "form_button_label",
            )
        }),
    )


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")
    list_editable = ("is_read",)

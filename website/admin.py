from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AboutPage,
    AboutTimelineItem,
    ContactPage,
    FooterContent,
    FooterQuickLink,
    FooterSocialLink,
    HomeFeature,
    HomeHeroSlide,
    HomePage,
    HomeTrustItem,
    AboutHeroImage,
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


class HomeTrustItemInline(admin.TabularInline):
    model = HomeTrustItem
    extra = 1
    fields = ("title", "order", "is_active")


class HomeHeroSlideInline(admin.StackedInline):
    model = HomeHeroSlide
    extra = 0
    verbose_name_plural = "Hero slides (shown in order; the video plays if there are none)"
    readonly_fields = ("desktop_preview", "tablet_preview", "mobile_preview")
    fieldsets = (
        (None, {
            "fields": (("order", "is_active"), "alt_text", ("display", "focus")),
        }),
        ("Desktop (1280 px and wider)", {
            "fields": ("image", "desktop_preview"),
        }),
        ("Tablet (768 to 1279 px) - optional", {
            "fields": ("tablet_image", "tablet_preview"),
        }),
        ("Phone (below 768 px) - optional", {
            "fields": ("mobile_image", "mobile_preview"),
        }),
    )

    @staticmethod
    def _preview(field_file, height):
        if not field_file:
            return "No image uploaded"
        return format_html(
            '<img src="{}" style="height:{}px;width:auto;border-radius:6px;border:1px solid #ddd;" />',
            field_file.url,
            height,
        )

    @admin.display(description="Preview")
    def desktop_preview(self, obj):
        return self._preview(obj.image, 110)

    @admin.display(description="Preview")
    def tablet_preview(self, obj):
        return self._preview(obj.tablet_image, 130)

    @admin.display(description="Preview")
    def mobile_preview(self, obj):
        return self._preview(obj.mobile_image, 160)


@admin.register(HomePage)
class HomePageAdmin(SingletonPageAdmin):
    inlines = [HomeHeroSlideInline, HomeFeatureInline, HomeTrustItemInline]
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
                "brands_description",
                "categories_eyebrow",
                "categories_title",
            )
        }),
        ("Trust Section", {
            "fields": ("trust_eyebrow", "trust_title")
        }),
        ("CTA Section", {
            "fields": ("cta_eyebrow", "cta_title", "cta_button_label")
        }),
    )


class AboutTimelineItemInline(admin.TabularInline):
    model = AboutTimelineItem
    extra = 1
    fields = ("title", "description", "order", "is_active")


class AboutHeroImageInline(admin.TabularInline):
    model = AboutHeroImage
    extra = 1
    fields = ("image", "order", "is_active")


@admin.register(AboutPage)
class AboutPageAdmin(SingletonPageAdmin):
    inlines = [AboutHeroImageInline, AboutTimelineItemInline]
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
        ("Map Location", {
            "fields": (
                "location_eyebrow",
                "location_title",
                "location_description",
                "location_map_url",
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
        ("Map", {
            "fields": (
                "map_title",
                "map_description",
                "google_maps_embed_url",
            )
        }),
    )


class FooterQuickLinkInline(admin.TabularInline):
    model = FooterQuickLink
    extra = 1
    fields = ("label", "url", "order", "is_active")


class FooterSocialLinkInline(admin.TabularInline):
    model = FooterSocialLink
    extra = 1
    fields = ("label", "url", "order", "is_active")


@admin.register(FooterContent)
class FooterContentAdmin(SingletonPageAdmin):
    inlines = [FooterQuickLinkInline, FooterSocialLinkInline]
    fieldsets = (
        ("Brand Section", {
            "fields": ("brand_title", "brand_description")
        }),
        ("Section Titles", {
            "fields": ("quick_links_title", "contact_title")
        }),
        ("Contact Information", {
            "fields": ("address", "email", "phone", "telephone")
        }),
        ("Bottom Bar", {
            "fields": ("copyright_text", "bottom_note")
        }),
    )

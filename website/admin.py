from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from products.models import Product
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
    ShowcaseItem,
    ShowcaseTab,
)


class SingletonPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class HomeFeatureInline(admin.TabularInline):
    model = HomeFeature
    extra = 1
    fields = ("title", "icon", "description", "order", "is_active")


class HomeTrustItemInline(admin.TabularInline):
    model = HomeTrustItem
    extra = 1
    fields = ("title", "order", "is_active")


class HomeHeroSlideInline(admin.StackedInline):
    model = HomeHeroSlide
    extra = 0
    verbose_name_plural = "Hero slides (shown in order)"
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
            "fields": ("intro_eyebrow", "intro_title", "intro_description")
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
                "email_2",
                "phone_label",
                "phone",
                "phone_2",
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
            "fields": ("address", "email", "email_2", "phone", "telephone")
        }),
        ("Bottom Bar", {
            "fields": ("copyright_text", "bottom_note")
        }),
        ("Background Image", {
            "fields": ("background_image", "background_shade")
        }),
    )


# ---------------------------------------------------------------------------
# Home product showcase (Best Sellers / Featured / New Launches)
#
# Editor workflow on each tab:
#   Step 1 - pick existing products in the two-box selector and save.
#   Step 2 - the chosen products are listed below; type their positions and save.
# ---------------------------------------------------------------------------

class ShowcaseProductChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, product):
        label = f"{product.name} - {product.company.name}"
        if not product.is_available:
            label += " (not available)"
        elif not product.image:
            label += " (no main image yet)"
        return label


class ShowcaseTabForm(forms.ModelForm):
    selected_products = ShowcaseProductChoiceField(
        label="Products",
        queryset=Product.objects.select_related("company").order_by("name"),
        required=False,
        widget=FilteredSelectMultiple("products", is_stacked=False),
        help_text=(
            "Click a product on the left and press the arrow to add it to this tab. "
            "To remove one, click it on the right and press the back arrow. "
            "Products marked \"not available\" are not shown on the website."
        ),
    )

    class Meta:
        model = ShowcaseTab
        fields = ("name", "subtitle", "is_active", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["selected_products"].initial = list(
                self.instance.items.values_list("product_id", flat=True)
            )


class ShowcaseItemInline(admin.TabularInline):
    model = ShowcaseItem
    extra = 0
    can_delete = False
    verbose_name = "chosen product"
    verbose_name_plural = (
        "Step 2 - Set the order (1 shows first). "
        "Newly chosen products appear here after you save."
    )
    fields = ("order", "image_preview", "product_details", "website_status")
    readonly_fields = ("image_preview", "product_details", "website_status")
    ordering = ("order", "id")

    # Products are only added or removed with the selector above, so there is
    # one clear way to do it
    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "product__company", "product__category"
        )

    @admin.display(description="Image")
    def image_preview(self, item):
        if not item.product.image:
            return "-"
        return format_html(
            '<img src="{}" alt="" style="height:64px;width:64px;object-fit:contain;'
            'background:#fff;border:1px solid #ddd;border-radius:6px;">',
            item.product.image.url,
        )

    @admin.display(description="Product")
    def product_details(self, item):
        product = item.product
        url = reverse("admin:products_product_change", args=[product.pk])
        details = " / ".join(
            name for name in (product.company.name, product.category.name) if name
        )
        return format_html(
            '<a href="{}"><strong>{}</strong></a><br><span style="color:#777;">{}</span>',
            url,
            product.name,
            details,
        )

    @admin.display(description="On website")
    def website_status(self, item):
        if not item.product.is_available:
            reason = "Hidden - product is marked not available"
        elif not item.product.image:
            reason = "Hidden - add the product's main image first"
        else:
            return format_html('<strong style="color:#2e7d32;">{}</strong>', "Shown")
        return format_html('<strong style="color:#c62828;">{}</strong>', reason)


@admin.register(ShowcaseTab)
class ShowcaseTabAdmin(admin.ModelAdmin):
    form = ShowcaseTabForm
    inlines = [ShowcaseItemInline]
    list_display = ("name", "products_chosen", "is_active", "order")
    list_editable = ("is_active", "order")
    fieldsets = (
        ("Tab settings", {
            "fields": ("name", "subtitle", ("is_active", "order")),
        }),
        ("Step 1 - Choose products for this tab", {
            "description": (
                "Only products you have already added under Products are listed. "
                "After choosing, press Save - you stay on this page to set their order below."
            ),
            "fields": ("selected_products",),
        }),
    )

    # The three tabs come from a migration; editors only change them
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("items"))

    @admin.display(description="Products chosen", ordering="product_count")
    def products_chosen(self, tab):
        return tab.product_count

    def save_related(self, request, form, formsets, change):
        # Saves the typed positions first, then applies the selector
        super().save_related(request, form, formsets, change)
        tab = form.instance
        chosen = list(form.cleaned_data.get("selected_products") or [])
        chosen_ids = {product.pk for product in chosen}

        tab.items.exclude(product_id__in=chosen_ids).delete()

        existing_ids = set(tab.items.values_list("product_id", flat=True))
        items = list(tab.items.order_by("order", "id"))
        # Newly chosen products go to the end of the list
        items += [
            ShowcaseItem(tab=tab, product=product)
            for product in chosen
            if product.pk not in existing_ids
        ]

        # Renumber 1, 2, 3... so the positions always read cleanly
        for position, item in enumerate(items, start=1):
            if item.pk is None or item.order != position:
                item.order = position
                item.save()

    def response_change(self, request, obj):
        # Plain "Save" stays on the tab, so the order of newly chosen
        # products can be set straight away
        if "_continue" not in request.POST:
            request.POST = request.POST.copy()
            request.POST["_continue"] = "1"
        return super().response_change(request, obj)

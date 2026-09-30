from django.contrib import admin
from .models import Product,ProductSize,ProductImage

# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    verbose_name = "Gallery image"
    verbose_name_plural = "Gallery images (shown under the main image)"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "company_line", "category", "size", "is_available")
    list_filter = ("company", "company_line", "category", "is_available")
    search_fields = ("name", "size", "company__name", "company_line__name", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    fieldsets = (
        ("Product", {
            "fields": (
                "name",
                "slug",
                ("company", "company_line", "category"),
                "description",
                "size",
                "is_available",
            )
        }),
        ("Media", {
            "fields": ("image", "youtube_url"),
        }),
        ("SEO (optional - leave empty to generate automatically)", {
            "fields": ("meta_title", "meta_description"),
        }),
    )


admin.site.register(ProductSize)
admin.site.register(ProductImage)

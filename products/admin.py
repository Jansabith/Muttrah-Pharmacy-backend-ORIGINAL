from django.contrib import admin
from .models import Product,ProductSize,ProductImage

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "company_line", "category", "size", "is_available")
    list_filter = ("company", "company_line", "category", "is_available")
    search_fields = ("name", "size", "company__name", "company_line__name", "category__name")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ProductSize)
admin.site.register(ProductImage)


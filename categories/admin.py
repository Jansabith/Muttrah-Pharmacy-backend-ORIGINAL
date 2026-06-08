from django.contrib import admin

from .models import Category

# Register your models here.




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "company_line", "slug")
    list_filter = ("company", "company_line")
    search_fields = ("name", "company__name", "company_line__name")

from django.contrib import admin

from .models import Company, CompanyLine

# Register your models here.

class CompanyLineInline(admin.TabularInline):
    model = CompanyLine
    extra = 1
    fields = ('name', 'description', 'is_active', 'display_order')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CompanyLineInline]


@admin.register(CompanyLine)
class CompanyLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active', 'display_order')
    list_filter = ('company', 'is_active')
    search_fields = ('name', 'company__name')

from django.contrib import admin

from .models import Company, CompanyLine

# Register your models here.

class CompanyLineInline(admin.TabularInline):
    model = CompanyLine
    extra = 1
    fields = ('name', 'slug', 'description', 'is_active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    fields = ('name', 'slug', 'logo', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CompanyLineInline]


@admin.register(CompanyLine)
class CompanyLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'slug', 'is_active', 'display_order')
    list_filter = ('company', 'is_active')
    search_fields = ('name', 'company__name')
    prepopulated_fields = {'slug': ('name',)}

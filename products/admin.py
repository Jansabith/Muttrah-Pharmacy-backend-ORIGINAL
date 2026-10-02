import secrets

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join

from . import importer
from .models import Product,ProductSize,ProductImage

IMPORT_SESSION_KEY = 'product_import_preview'

# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    verbose_name = "Gallery image"
    verbose_name_plural = "Gallery images (shown under the main image)"


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_image(self):
        # The model allows an empty image only for the Excel import; a product
        # added by hand still needs its main image
        image = self.cleaned_data.get("image")
        if not image and not self.instance.pk:
            raise forms.ValidationError("Please upload the main image.")
        return image


class HasMainImageFilter(admin.SimpleListFilter):
    title = "has main image"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes - shown on website"),
            ("no", "No - hidden until image added"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(image="")
        if self.value() == "no":
            return queryset.filter(image="")
        return queryset


class ProductImportForm(forms.Form):
    file = forms.FileField(
        label="Filled Excel file",
        help_text="The downloaded template, filled in (.xlsx). A .csv file also works.",
    )

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        name = (uploaded.name or "").lower()
        if not name.endswith((".xlsx", ".csv")):
            raise forms.ValidationError("Please upload an Excel (.xlsx) or CSV file.")
        if uploaded.size > importer.MAX_FILE_SIZE:
            raise forms.ValidationError("The file is too large (maximum 5 MB).")
        return uploaded


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "company", "company_line", "category", "size", "has_main_image", "is_available")
    list_filter = (HasMainImageFilter, "company", "company_line", "category", "is_available")
    search_fields = ("name", "size", "company__name", "company_line__name", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    readonly_fields = ("home_showcase",)
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
        ("Home page showcase", {
            "fields": ("home_showcase",),
        }),
    )

    @admin.display(description="Main image", boolean=True, ordering="image")
    def has_main_image(self, product):
        return bool(product.image)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.image:
            messages.warning(
                request,
                f'"{obj.name}" is hidden on the website until you add its main image.',
            )

    # ---- Excel import -----------------------------------------------------

    def get_urls(self):
        # Before the default URLs, which would read "import" as a product id
        return [
            path(
                "import/",
                self.admin_site.admin_view(self.import_view),
                name="products_product_import",
            ),
            path(
                "import/template/",
                self.admin_site.admin_view(self.import_template_view),
                name="products_product_import_template",
            ),
        ] + super().get_urls()

    def _check_import_permission(self, request):
        if not (self.has_add_permission(request) and self.has_change_permission(request)):
            raise PermissionDenied

    def import_template_view(self, request):
        self._check_import_permission(request)
        response = HttpResponse(
            importer.build_template(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="products_import_template.xlsx"'
        return response

    def import_view(self, request):
        """Step 1 upload, step 2 preview, step 3 confirm. The checked rows wait
        in the session between preview and confirm, so nothing is saved until
        the editor confirms."""
        self._check_import_permission(request)
        import_url = reverse("admin:products_product_import")
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Import products from Excel",
            "template_url": reverse("admin:products_product_import_template"),
            "max_rows": importer.MAX_ROWS,
        }

        if request.method == "POST" and request.POST.get("action") == "confirm":
            pending = request.session.get(IMPORT_SESSION_KEY)
            if not pending or pending.get("token") != request.POST.get("token"):
                messages.error(request, "This preview has expired. Please upload the file again.")
                return redirect(import_url)
            try:
                created, updated = importer.apply_rows(pending["results"])
            except importer.ImportAborted as error:
                messages.error(request, str(error))
                return redirect(import_url)
            request.session.pop(IMPORT_SESSION_KEY, None)
            messages.success(
                request,
                f"Import finished: {created} new product(s) added, {updated} updated. "
                "New products stay hidden on the website until you add their main image.",
            )
            changelist = reverse("admin:products_product_changelist")
            return redirect(f"{changelist}?has_image=no" if created else changelist)

        if request.method == "POST":
            form = ProductImportForm(request.POST, request.FILES)
            if form.is_valid():
                rows, file_error = importer.read_file(form.cleaned_data["file"])
                if file_error:
                    form.add_error("file", file_error)
                else:
                    results = importer.validate_rows(rows)
                    summary = importer.summarize(results)
                    context.update(results=results, summary=summary)
                    if not summary["error"]:
                        token = secrets.token_urlsafe(16)
                        request.session[IMPORT_SESSION_KEY] = {"token": token, "results": results}
                        context["token"] = token
        else:
            form = ProductImportForm()
            request.session.pop(IMPORT_SESSION_KEY, None)

        context["form"] = form
        return TemplateResponse(request, "admin/products/product/import.html", context)

    @admin.display(description="Shown in tabs")
    def home_showcase(self, product):
        manage_url = reverse("admin:website_showcasetab_changelist")
        manage_link = format_html(
            '<a href="{}">Manage Best Sellers / Featured / New Launches</a>', manage_url
        )
        items = product.showcase_items.select_related("tab") if product.pk else []
        tabs = format_html_join(", ", "{} (position {})", ((i.tab.name, i.order) for i in items))
        if not tabs:
            return format_html("Not in any tab. {}", manage_link)
        return format_html("{}. {}", tabs, manage_link)


admin.site.register(ProductSize)
admin.site.register(ProductImage)

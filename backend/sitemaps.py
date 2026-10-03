from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap

from categories.models import Category
from companies.models import Company
from products.models import Product

# Set FRONTEND_URL=https://muttrahpharmacy.com in the server's .env so the
# sitemap links point to the live website.
FRONTEND = urlparse(settings.FRONTEND_URL)


class FrontendSitemap(Sitemap):
    """Links point to the React website, not to this API server's own domain."""

    protocol = FRONTEND.scheme or "https"

    def get_domain(self, site=None):
        return FRONTEND.netloc


class StaticPagesSitemap(FrontendSitemap):
    pages = {
        "/": ("weekly", 1.0),
        "/products": ("daily", 0.9),
        "/about": ("monthly", 0.7),
        "/contact": ("monthly", 0.7),
    }

    def items(self):
        return list(self.pages)

    def location(self, item):
        return item

    def changefreq(self, item):
        return self.pages[item][0]

    def priority(self, item):
        return self.pages[item][1]


class CompanySitemap(FrontendSitemap):
    """One URL per brand, e.g. /products?company=tynor."""

    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Company.objects.order_by("id")

    def location(self, company):
        return f"/products?company={company.slug}"


class CategorySitemap(FrontendSitemap):
    """One URL per category: /products?company=<brand>&category=<category>
    for categories that belong to a brand, or /products?category=<category>
    for the few that do not (matches how the website links to them)."""

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.select_related("company").order_by("id")

    def location(self, category):
        if category.company_id:
            return f"/products?company={category.company.slug}&category={category.slug}"
        return f"/products?category={category.slug}"


class ProductSitemap(FrontendSitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Only products the website shows (they need a main image)
        return Product.objects.with_main_image().order_by("id")

    def location(self, product):
        # Matches the React route /products/:slug
        return f"/products/{product.slug}"

    def lastmod(self, product):
        return product.updated_at


sitemaps = {
    "pages": StaticPagesSitemap,
    "brands": CompanySitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
}

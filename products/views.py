from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.text import Truncator
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .models import Product
from .serializers import ProductSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'company__name', 'company_line__name', 'category__name']

    def get_queryset(self):

        queryset = Product.objects.select_related(
            'company',
            'company_line',
            'category'
        ).prefetch_related('gallery').all()

        company = self.request.GET.get("company")

        company_line = self.request.GET.get("company_line")

        category = self.request.GET.get("category")

        if company:
            queryset = queryset.filter(
                company_id=company
            )

        if company_line:
            queryset = queryset.filter(
                company_line_id=company_line
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        return queryset
    
def product_share_preview(request, slug):
    """Link-preview page for WhatsApp, Facebook, etc.

    Chat apps don't run the React app's JavaScript, so they can't see each
    product's title and image. This page gives them those tags directly and
    forwards real visitors to the product page on the website.
    """
    product = get_object_or_404(Product, slug=slug)

    title = product.meta_title or product.name
    if 'muttrah pharmacy' not in title.lower():
        title = f'{title} | Muttrah Pharmacy'
    description = product.meta_description or Truncator(product.description).chars(155)

    image_url = request.build_absolute_uri(product.image.url) if product.image else ''
    page_url = f"{settings.FRONTEND_URL.rstrip('/')}/products/{product.slug}"

    return render(request, 'products/share_preview.html', {
        'product': product,
        'title': title,
        'description': description,
        'image_url': image_url,
        'page_url': page_url,
    })


class ProductDetailAPIView(RetrieveAPIView):

    queryset = Product.objects.prefetch_related('gallery').all()

    serializer_class = ProductSerializer

    lookup_field = 'slug'

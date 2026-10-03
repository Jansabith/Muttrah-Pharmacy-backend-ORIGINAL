from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.text import Truncator
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, IntegerField, Q, Value, When
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.filters import by_slug_or_id
from categories.models import Category
from companies.models import Company
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

        # Products without a main image (e.g. just imported from Excel) stay hidden
        queryset = Product.objects.with_main_image().select_related(
            'company',
            'company_line',
            'category'
        ).prefetch_related('gallery')

        company = self.request.GET.get("company")

        company_line = self.request.GET.get("company_line")

        category = self.request.GET.get("category")

        # Each accepts the name in the address (?company=tynor) or an old number
        if company:
            queryset = queryset.filter(by_slug_or_id('company', company))

        if company_line:
            queryset = queryset.filter(by_slug_or_id('company_line', company_line))

        if category:
            queryset = queryset.filter(by_slug_or_id('category', category))

        return queryset
    
SUGGEST_MIN_LENGTH = 2
SUGGEST_PRODUCT_LIMIT = 6
SUGGEST_GROUP_LIMIT = 4


class ProductSuggestAPIView(APIView):
    """Live search for the navbar: a few ranked products plus matching brands
    and categories. Returns only what the dropdown shows, to stay fast."""

    def get(self, request):
        query = ' '.join(request.GET.get('q', '').split())[:80]
        if len(query) < SUGGEST_MIN_LENGTH:
            return Response({'query': query, 'count': 0, 'products': [], 'brands': [], 'categories': []})

        # Every word must match somewhere (name, brand, line or category)
        matches = Q()
        for term in query.split():
            matches &= (
                Q(name__icontains=term)
                | Q(company__name__icontains=term)
                | Q(company_line__name__icontains=term)
                | Q(category__name__icontains=term)
            )
        queryset = Product.objects.with_main_image().filter(matches)

        # Names starting with the search come first, then names containing it
        ranked = queryset.select_related('company', 'category').annotate(
            rank=Case(
                When(name__istartswith=query, then=Value(0)),
                When(name__icontains=query, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('rank', 'name')[:SUGGEST_PRODUCT_LIMIT]

        products = [
            {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'image': request.build_absolute_uri(product.image.url) if product.image else '',
                'company_name': product.company.name,
                'category_name': product.category.name,
            }
            for product in ranked
        ]
        brands = [
            {'id': company.id, 'slug': company.slug, 'name': company.name}
            for company in Company.objects.filter(name__icontains=query).order_by('name')[:SUGGEST_GROUP_LIMIT]
        ]
        categories = [
            {
                'id': category.id,
                'slug': category.slug,
                'name': category.name,
                'company_name': category.company.name if category.company else '',
            }
            for category in Category.objects.filter(name__icontains=query)
            .select_related('company')
            .order_by('name')[:SUGGEST_GROUP_LIMIT]
        ]

        return Response({
            'query': query,
            'count': queryset.count(),
            'products': products,
            'brands': brands,
            'categories': categories,
        })


def product_share_preview(request, slug):
    """Link-preview page for WhatsApp, Facebook, etc.

    Chat apps don't run the React app's JavaScript, so they can't see each
    product's title and image. This page gives them those tags directly and
    forwards real visitors to the product page on the website.
    """
    product = get_object_or_404(Product.objects.with_main_image(), slug=slug)

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

    queryset = Product.objects.with_main_image().select_related(
        'company', 'category'
    ).prefetch_related('gallery')

    serializer_class = ProductSerializer

    lookup_field = 'slug'

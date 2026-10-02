from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductSuggestAPIView,
)

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),

    # Must come before the slug route, or "suggest" is read as a product slug
    path('suggest/', ProductSuggestAPIView.as_view(), name='product-suggest'),

    path(
        '<slug:slug>/',
        ProductDetailAPIView.as_view(),
        name='product-detail'
    ),
]
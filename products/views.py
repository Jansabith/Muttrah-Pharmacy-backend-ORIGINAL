from django.shortcuts import render

from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import Product
from .serializers import ProductSerializer  
# Create your views here.
class ProductListAPIView(ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.all()

        company = self.request.GET.get("company")

        category = self.request.GET.get("category")

        if company:
            queryset = queryset.filter(
                company_id=company
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        return queryset
    
class ProductDetailAPIView(RetrieveAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer




from django.shortcuts import render

from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import Product
from .serializers import ProductSerializer  
# Create your views here.
class ProductListAPIView(ListAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.select_related(
            'company',
            'company_line',
            'category'
        ).all()

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
    
class ProductDetailAPIView(RetrieveAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer




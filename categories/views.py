from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView

from .models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.select_related(
            'company',
            'company_line'
        ).all()

        company = self.request.GET.get("company")
        company_line = self.request.GET.get("company_line")

        if company:
            queryset = queryset.filter(
                company_id=company
            )

        if company_line:
            queryset = queryset.filter(
                company_line_id=company_line
            )

        return queryset

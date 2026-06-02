from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView

from .models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer
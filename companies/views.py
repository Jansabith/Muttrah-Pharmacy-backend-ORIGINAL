from django.shortcuts import render
from rest_framework import ListAPIView

from .models import Company
from .serializers import CompanySerializer

class CompanyListAPIView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer    

    


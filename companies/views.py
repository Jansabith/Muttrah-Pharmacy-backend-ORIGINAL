from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import Company
from .serializers import CompanySerializer

class CompanyListAPIView(ListAPIView):
    queryset = Company.objects.prefetch_related('lines').all()
    serializer_class = CompanySerializer    

    

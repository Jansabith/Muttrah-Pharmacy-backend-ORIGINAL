from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from products.models import Product
from .models import AboutPage, ContactPage, FooterContent, HomePage
from .serializers import (
    AboutPageSerializer,
    ContactPageSerializer,
    FooterContentSerializer,
    HomePageSerializer,
)


class HomePageAPIView(RetrieveAPIView):
    serializer_class = HomePageSerializer

    def get_object(self):
        return HomePage.load()


class AboutPageAPIView(RetrieveAPIView):
    serializer_class = AboutPageSerializer

    def get_object(self):
        return AboutPage.load()


class ContactPageAPIView(RetrieveAPIView):
    serializer_class = ContactPageSerializer

    def get_object(self):
        return ContactPage.load()


class FooterContentAPIView(RetrieveAPIView):
    serializer_class = FooterContentSerializer

    def get_object(self):
        return FooterContent.load()


from django.conf import settings

def sitemap_view(request):
    products = Product.objects.all()
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173').rstrip('/')
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Static pages
    for page in ['', '/about', '/contact', '/products']:
        xml.append(f'  <url><loc>{frontend_url}{page}</loc></url>')
        
    # Dynamic products
    for product in products:
        if product.slug:
            xml.append(f'  <url><loc>{frontend_url}/products/{product.slug}</loc></url>')
        
    xml.append('</urlset>')
    
    return HttpResponse('\n'.join(xml), content_type='application/xml')


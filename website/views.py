from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.http import HttpResponse
from products.models import Product
from .models import AboutPage, ContactPage, ContactSubmission, FooterContent, HomePage
from .serializers import (
    AboutPageSerializer,
    ContactPageSerializer,
    ContactSubmissionSerializer,
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


from django.core.mail import send_mail
from django.conf import settings

class ContactSubmissionCreateAPIView(CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

    def perform_create(self, serializer):
        submission = serializer.save()
        
        # Get the configured email recipient
        contact_page = ContactPage.load()
        recipient_email = contact_page.inquiry_recipient_email
        
        if recipient_email:
            subject = f"New Contact Inquiry from {submission.name}"
            message = (
                f"Name: {submission.name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone}\n\n"
                f"Message:\n{submission.message}\n"
            )
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'webmaster@localhost',
                    recipient_list=[recipient_email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error or handle it silently to not break the API response
                print(f"Failed to send email: {e}")

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


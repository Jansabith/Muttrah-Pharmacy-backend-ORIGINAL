from rest_framework.generics import CreateAPIView, RetrieveAPIView
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

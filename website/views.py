from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import AboutPage, ContactPage, ContactSubmission, HomePage
from .serializers import (
    AboutPageSerializer,
    ContactPageSerializer,
    ContactSubmissionSerializer,
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


class ContactSubmissionCreateAPIView(CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

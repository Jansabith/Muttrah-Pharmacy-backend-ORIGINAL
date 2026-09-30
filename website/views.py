from rest_framework.generics import RetrieveAPIView
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


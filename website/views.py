from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AboutPage, ContactPage, FooterContent, HomePage, ShowcaseItem, ShowcaseTab
from .serializers import (
    AboutPageSerializer,
    ContactPageSerializer,
    FooterContentSerializer,
    HomePageSerializer,
    ShowcaseTabSerializer,
)


class HomePageAPIView(RetrieveAPIView):
    serializer_class = HomePageSerializer

    def get_object(self):
        return HomePage.load()


class ShowcaseAPIView(APIView):
    """Home page product showcase: visible tabs in order, each with its
    available products in the positions set in the admin. Empty tabs are left out."""

    def get(self, request):
        items = (
            ShowcaseItem.objects.filter(product__is_available=True)
            .exclude(product__image="")
            .select_related("product__company", "product__company_line", "product__category")
            .prefetch_related("product__gallery")
            .order_by("order", "id")
        )
        tabs = ShowcaseTab.objects.filter(is_active=True).prefetch_related(
            Prefetch("items", queryset=items)
        )
        data = ShowcaseTabSerializer(tabs, many=True, context={"request": request}).data
        return Response([tab for tab in data if tab["products"]])


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


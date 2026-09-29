from django.urls import path
from .views import (
    AboutPageAPIView,
    ContactPageAPIView,
    FooterContentAPIView,
    HomePageAPIView,
    sitemap_view,
)

urlpatterns = [
    path("home/", HomePageAPIView.as_view(), name="website-home"),
    path("about/", AboutPageAPIView.as_view(), name="website-about"),
    path("contact/", ContactPageAPIView.as_view(), name="website-contact"),
    path("footer/", FooterContentAPIView.as_view(), name="website-footer"),
    path("sitemap.xml", sitemap_view, name="sitemap"),
]

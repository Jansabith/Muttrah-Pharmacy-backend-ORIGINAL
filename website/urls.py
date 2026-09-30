from django.contrib.sitemaps.views import sitemap
from django.urls import path

from backend.sitemaps import sitemaps
from .views import (
    AboutPageAPIView,
    ContactPageAPIView,
    FooterContentAPIView,
    HomePageAPIView,
)

urlpatterns = [
    path("home/", HomePageAPIView.as_view(), name="website-home"),
    path("about/", AboutPageAPIView.as_view(), name="website-about"),
    path("contact/", ContactPageAPIView.as_view(), name="website-contact"),
    path("footer/", FooterContentAPIView.as_view(), name="website-footer"),
    # Older address for the sitemap; serves the same sitemap as /sitemap.xml
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

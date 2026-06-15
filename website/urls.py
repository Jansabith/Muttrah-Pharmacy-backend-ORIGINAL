from django.urls import path
from .views import (
    AboutPageAPIView,
    ContactPageAPIView,
    ContactSubmissionCreateAPIView,
    FooterContentAPIView,
    HomePageAPIView,
)

urlpatterns = [
    path("home/", HomePageAPIView.as_view(), name="website-home"),
    path("about/", AboutPageAPIView.as_view(), name="website-about"),
    path("contact/", ContactPageAPIView.as_view(), name="website-contact"),
    path("footer/", FooterContentAPIView.as_view(), name="website-footer"),
    path("contact-submit/", ContactSubmissionCreateAPIView.as_view(), name="contact-submit"),
]

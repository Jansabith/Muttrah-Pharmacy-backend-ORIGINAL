from django.urls import path
from .views import (
    AboutPageAPIView,
    ContactPageAPIView,
    ContactSubmissionCreateAPIView,
    HomePageAPIView,
)

urlpatterns = [
    path("home/", HomePageAPIView.as_view(), name="website-home"),
    path("about/", AboutPageAPIView.as_view(), name="website-about"),
    path("contact/", ContactPageAPIView.as_view(), name="website-contact"),
    path("contact-submit/", ContactSubmissionCreateAPIView.as_view(), name="contact-submit"),
]

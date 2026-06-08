from django.urls import path
from .views import ContactSubmissionCreateAPIView

urlpatterns = [
    path("", ContactSubmissionCreateAPIView.as_view(), name="contact"),
]

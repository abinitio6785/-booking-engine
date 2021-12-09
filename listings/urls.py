"""
RestInterface/urls.py
"""
from django.urls import path

from listings.views import BookingInfoViewSet

urlpatterns = [
    path('units/', BookingInfoViewSet.as_view())
]

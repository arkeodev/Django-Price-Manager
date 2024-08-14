"""
URL configuration module for the Event application.

This module defines the URL patterns for accessing and manipulating Event-related views.
"""

from typing import List

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import EventView

# Define the URL patterns for the Event related views.
urlpatterns: List[URLPattern] = [
    # Endpoint for accessing and manipulating event data via the EventView.
    path("events/", EventView.as_view(), name="events"),
]

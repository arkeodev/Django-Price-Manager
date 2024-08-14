"""
URL configuration module for the Dashboard application.

This module defines the URL patterns for accessing and manipulating Dashboard-related views.
"""

from typing import List

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import DashboardView

# Define the URL patterns for the Dashboard related views.
urlpatterns: List[URLPattern] = [
    # Endpoint for accessing and manipulating dashboard data via the DashboardView.
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]

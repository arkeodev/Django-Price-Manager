from typing import Any

from rest_framework import generics

from .models import DashboardData
from .serializers import DashboardDataSerializer


class DashboardView(generics.ListAPIView):
    """
    API view to retrieve dashboard data for a hotel.

    Supports filtering based on hotel ID, period, and year.
    """

    serializer_class = DashboardDataSerializer

    def get_queryset(self) -> Any:
        """
        Override get_queryset to apply filtering based on query parameters.
        """
        queryset = DashboardData.objects.all()
        hotel_id = self.request.query_params.get("hotel_id")
        period = self.request.query_params.get("period")
        year = self.request.query_params.get("year")

        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
        if period:
            queryset = queryset.filter(period=period)
        if year:
            queryset = queryset.filter(year=year)

        return queryset

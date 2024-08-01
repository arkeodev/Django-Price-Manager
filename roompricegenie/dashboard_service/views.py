from rest_framework import generics

from .models import DashboardData
from .serializers import DashboardDataSerializer


class DashboardView(generics.ListAPIView):
    serializer_class = DashboardDataSerializer

    def get_queryset(self):
        hotel_id = self.request.query_params.get("hotel_id")
        period = self.request.query_params.get("period")
        year = self.request.query_params.get("year")
        queryset = DashboardData.objects.filter(
            hotel_id=hotel_id, period=period, year=year
        )

        if period == "month":
            queryset = (
                queryset.values("year", "month")
                .annotate(total_bookings=Sum("booking_count"))
                .order_by("year", "month")
            )
        elif period == "day":
            queryset = queryset.order_by("year", "month", "day")

        return queryset

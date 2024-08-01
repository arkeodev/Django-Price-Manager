from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, response

from .models import DashboardData
from .serializers import DashboardDataSerializer


class DashboardView(generics.ListAPIView):
    serializer_class = DashboardDataSerializer

    @swagger_auto_schema(
        operation_description="Retrieve dashboard data for a specific hotel and period",
        manual_parameters=[
            openapi.Parameter(
                "hotel_id",
                in_=openapi.IN_QUERY,
                description="Hotel ID for which to retrieve data",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "period",
                in_=openapi.IN_QUERY,
                description="Period of the data ('month' or 'day')",
                type=openapi.TYPE_STRING,
                enum=["month", "day"],
            ),
            openapi.Parameter(
                "year",
                in_=openapi.IN_QUERY,
                description="Year of the data to retrieve",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "month",
                in_=openapi.IN_QUERY,
                description="Month of the data to retrieve, required if period is 'month'",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "day",
                in_=openapi.IN_QUERY,
                description="Day of the data to retrieve, optional, only relevant if period is 'day'",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        hotel_id = request.query_params.get("hotel_id")
        period = request.query_params.get("period")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")

        dashboard_objects = DashboardData.objects.all()
        if hotel_id:
            dashboard_objects = dashboard_objects.filter(hotel_id=hotel_id)
        if period:
            dashboard_objects = dashboard_objects.filter(period=period)
        if year:
            dashboard_objects = dashboard_objects.filter(year=year)
        if month:
            dashboard_objects = dashboard_objects.filter(month=month)
        if day and period == "day":  # Ensure 'day' is considered only for 'day' period
            dashboard_objects = dashboard_objects.filter(day=day)

        serializer = DashboardDataSerializer(dashboard_objects, many=True)
        return response.Response(serializer.data)

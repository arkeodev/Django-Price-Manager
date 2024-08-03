"""
Module for handling dashboard views in the RoomPriceGenie project.

This module defines the views for retrieving dashboard data for specific hotels.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from .models import DashboardData
from .serializers import DashboardDataSerializer


class DashboardView(generics.ListAPIView):
    """
    API view to retrieve dashboard data for a specific hotel and period.

    This view supports querying dashboard data based on hotel ID, period (month or day),
    year, month, and day. The data is returned in JSON format.
    """

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
                minimum=1950,
                maximum=2050,
            ),
            openapi.Parameter(
                "month",
                in_=openapi.IN_QUERY,
                description="Month of the data to retrieve, required if period is 'month'",
                type=openapi.TYPE_INTEGER,
                minimum=1,
                maximum=12,
            ),
            openapi.Parameter(
                "day",
                in_=openapi.IN_QUERY,
                description="Day of the data to retrieve, optional, only relevant if period is 'day'",
                type=openapi.TYPE_INTEGER,
                minimum=1,
                maximum=31,
                required=False,
            ),
        ],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve dashboard data.

        This method retrieves dashboard data based on the provided query parameters,
        such as hotel ID, period, year, month, and day. It validates the parameters
        and filters the data accordingly.

        Args:
            request (Request): The HTTP request object containing query parameters.

        Returns:
            Response: A response object containing the serialized dashboard data.
        """
        hotel_id = request.query_params.get("hotel_id")
        period = request.query_params.get("period")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")

        # Validate year, month, and day within the view
        try:
            if year and (int(year) < 1950 or int(year) > 2050):
                raise ValidationError("Year must be between 1950 and 2050.")
            if month and (int(month) < 1 or int(month) > 12):
                raise ValidationError("Month must be between 1 and 12.")
            if day and (int(day) < 1 or int(day) > 31):
                raise ValidationError("Day must be between 1 and 31.")
        except ValueError:
            return response.Response(
                {"error": "Invalid input for date parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter dashboard data based on provided query parameters
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

        # Serialize the filtered data
        serializer = DashboardDataSerializer(dashboard_objects, many=True)
        return response.Response(serializer.data)

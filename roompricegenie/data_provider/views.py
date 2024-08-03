"""
Event views module for handling Event-related HTTP requests and responses.

This module contains the views to handle GET and POST requests for Event objects,
including filtering and validation logic for query parameters.
"""

import logging
from typing import Any

from django.forms import ValidationError
from django.utils.dateparse import parse_date, parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer

logger = logging.getLogger("roompricegenie")


class EventView(generics.ListCreateAPIView):
    """
    View to handle GET and POST requests for Event objects.

    This view supports filtering Event objects based on various query parameters
    and provides validation for these parameters.
    """

    serializer_class = EventSerializer

    @swagger_auto_schema(
        operation_description="Get or create events",
        manual_parameters=[
            openapi.Parameter(
                "hotel_id",
                openapi.IN_QUERY,
                description="ID of the hotel",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "updated_gte",
                openapi.IN_QUERY,
                description="Events updated after or at this date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "updated_lte",
                openapi.IN_QUERY,
                description="Events updated before or at this date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "rpg_status",
                openapi.IN_QUERY,
                description="Status of the event (1 for booking, 2 for cancellation)",
                type=openapi.TYPE_INTEGER,
                enum=[1, 2],
            ),
            openapi.Parameter(
                "room_reservation_id",
                openapi.IN_QUERY,
                description="UUID of the room reservation",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
            ),
            openapi.Parameter(
                "night_of_stay_gte",
                openapi.IN_QUERY,
                description="Night of stay after or on this date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "night_of_stay_lte",
                openapi.IN_QUERY,
                description="Night of stay before or on this date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
        ],
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handles GET requests to retrieve events based on query parameters.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the filtered events.
        """
        hotel_id = request.query_params.get("hotel_id")
        rpg_status = request.query_params.get("rpg_status")
        room_reservation_id = request.query_params.get("room_reservation_id")
        updated_gte = request.query_params.get("updated_gte")
        updated_lte = request.query_params.get("updated_lte")
        night_of_stay_gte = request.query_params.get("night_of_stay_gte")
        night_of_stay_lte = request.query_params.get("night_of_stay_lte")

        # Start with all events
        events = Event.objects.all()

        # Apply filters conditionally
        if hotel_id:
            events = events.filter(hotel_id=hotel_id)
        if rpg_status:
            events = events.filter(rpg_status=rpg_status)
        if room_reservation_id:
            events = events.filter(room_reservation_id=room_reservation_id)

        # Parsing datetime fields
        if updated_gte:
            try:
                parsed_date_gte = parse_datetime(updated_gte)
                if parsed_date_gte:
                    events = events.filter(timestamp__gte=parsed_date_gte)
                    logger.info(
                        f"Filtering events updated after or at: {parsed_date_gte}"
                    )
            except ValidationError as e:
                logger.error(f"Error parsing date: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if updated_lte:
            try:
                parsed_date_lte = parse_datetime(updated_lte)
                if parsed_date_lte:
                    events = events.filter(timestamp__lte=parsed_date_lte)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Parsing date fields
        if night_of_stay_gte:
            try:
                parsed_night_gte = parse_date(night_of_stay_gte)
                if parsed_night_gte:
                    events = events.filter(night_of_stay__gte=parsed_night_gte)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if night_of_stay_lte:
            try:
                parsed_night_lte = parse_date(night_of_stay_lte)
                if parsed_night_lte:
                    events = events.filter(night_of_stay__lte=parsed_night_lte)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Order events by timestamp
        events = events.order_by("timestamp")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new event",
        request_body=EventSerializer,
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handles POST requests to create a new event.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response containing the created event data or errors.
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

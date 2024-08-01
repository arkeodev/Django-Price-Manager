from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer


class EventView(generics.ListCreateAPIView):
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
    def get(self, request, *args, **kwargs):
        hotel_id = request.query_params.get("hotel_id")
        updated_gte = request.query_params.get("updated__gte")
        updated_lte = request.query_params.get("updated__lte")
        rpg_status = request.query_params.get("rpg_status")
        room_reservation_id = request.query_params.get("room_reservation_id")
        night_of_stay_gte = request.query_params.get("night_of_stay__gte")
        night_of_stay_lte = request.query_params.get("night_of_stay__lte")

        events = Event.objects.all()
        if hotel_id:
            events = events.filter(hotel_id=hotel_id)
        if updated_gte:
            events = events.filter(timestamp__gte=updated_gte)
        if updated_lte:
            events = events.filter(timestamp__lte=updated_lte)
        if rpg_status:
            events = events.filter(rpg_status=rpg_status)
        if room_reservation_id:
            events = events.filter(room_reservation_id=room_reservation_id)
        if night_of_stay_gte:
            events = events.filter(night_of_stay__gte=night_of_stay_gte)
        if night_of_stay_lte:
            events = events.filter(night_of_stay__lte=night_of_stay_lte)

        events = events.order_by("timestamp")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new event", request_body=EventSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

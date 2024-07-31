from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer


@api_view(["GET", "POST"])
def events_view(request):
    if request.method == "GET":
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

    elif request.method == "POST":
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

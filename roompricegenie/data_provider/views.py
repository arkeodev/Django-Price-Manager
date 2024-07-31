# data_provider/views.py

from typing import Any

from rest_framework import generics

from .models import Event
from .serializers import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of events and create new events.

    Supports filtering events based on query parameters.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self) -> Any:
        """
        Override get_queryset to apply filtering based on query parameters.
        """
        queryset = super().get_queryset()
        hotel_id = self.request.query_params.get("hotel_id")
        updated_gte = self.request.query_params.get("updated__gte")
        updated_lte = self.request.query_params.get("updated__lte")
        rpg_status = self.request.query_params.get("rpg_status")
        room_id = self.request.query_params.get("room_id")
        night_of_stay_gte = self.request.query_params.get("night_of_stay__gte")
        night_of_stay_lte = self.request.query_params.get("night_of_stay__lte")

        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
        if updated_gte:
            queryset = queryset.filter(timestamp__gte=updated_gte)
        if updated_lte:
            queryset = queryset.filter(timestamp__lte=updated_lte)
        if rpg_status:
            queryset = queryset.filter(rpg_status=rpg_status)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        if night_of_stay_gte:
            queryset = queryset.filter(night_of_stay__gte=night_of_stay_gte)
        if night_of_stay_lte:
            queryset = queryset.filter(night_of_stay__lte=night_of_stay_lte)

        return queryset

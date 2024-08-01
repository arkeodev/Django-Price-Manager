from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    event_timestamp = serializers.DateTimeField(source="timestamp")
    status = serializers.IntegerField(source="rpg_status")

    class Meta:
        model = Event
        fields = [
            "id",
            "hotel_id",
            "event_timestamp",
            "status",
            "room_reservation_id",
            "night_of_stay",
        ]

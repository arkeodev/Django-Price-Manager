from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    event_timestamp = serializers.DateTimeField(source="timestamp", write_only=True)
    status = serializers.IntegerField(source="rpg_status", write_only=True)

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
        extra_kwargs = {
            "timestamp": {"read_only": True},
            "rpg_status": {"read_only": True},
        }

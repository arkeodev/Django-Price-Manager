from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.

    Provides validation and serialization for Event instances.
    """

    class Meta:
        model = Event
        fields = "__all__"

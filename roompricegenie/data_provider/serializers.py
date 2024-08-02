from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model that transforms model instances into JSON format
    and validates incoming data against the model's definition before saving.

    Attributes:
        event_timestamp (DateTimeField): A serializer field mapped to the 'timestamp' model field.
        status (IntegerField): A serializer field mapped to the 'rpg_status' model field to provide clarity in serialized data.

    Meta:
        model (Model): The model class that this serializer will serialize.
        fields (list of str): Specifies the fields to be included in the serialized output.
    """

    # Field redefinitions to provide more meaningful key names in the API output
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
        read_only_fields = ["id"]  # Making 'id' field read-only for additional safety

    def validate(self, data: dict) -> dict:
        """
        Validate incoming data to ensure it conforms to logical constraints beyond the model's field validations.

        Args:
            data (dict): The incoming data to validate.

        Returns:
            dict: The validated data, potentially with modifications.

        Raises:
            serializers.ValidationError: If any constraints are violated.
        """
        # Example custom validation logic
        if data["rpg_status"] not in [Event.BOOKING, Event.CANCELLATION]:
            raise serializers.ValidationError({"status": "Invalid status provided."})

        return data

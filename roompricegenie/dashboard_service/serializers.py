from rest_framework import serializers

from .models import DashboardData


class DashboardDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the DashboardData model.

    Provides validation and serialization for DashboardData instances.
    """

    day = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = DashboardData
        fields = "__all__"

    def to_internal_value(self, data):
        if data.get("period") == "month":
            data["day"] = None
        return super().to_internal_value(data)

    def validate(self, data):
        """
        Check that the day is provided if the period is 'day'.
        """
        if data["period"] == "day" and not data.get("day"):
            raise serializers.ValidationError(
                "Day is required when the period is 'day'."
            )
        return data

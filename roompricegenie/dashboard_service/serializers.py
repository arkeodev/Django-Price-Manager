"""
Serializer module for DashboardData model.

This module contains the serializer class for the DashboardData model which is responsible for
validating and transforming model instances into JSON format and vice versa.
"""

from typing import Any, Dict

from rest_framework import serializers

from .models import DashboardData


class DashboardDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the DashboardData model.

    Provides validation and serialization for DashboardData instances.

    Attributes:
        day (IntegerField): An optional field for the day, required only if the period is 'day'.
    """

    day = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = DashboardData
        fields = "__all__"

    def to_internal_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert the input data into a validated internal value.

        Args:
            data (Dict[str, Any]): The input data to validate and convert.

        Returns:
            Dict[str, Any]: The validated internal data.
        """
        if data.get("period") == "month":
            data["day"] = None  # Set day to None if the period is 'month'
        return super().to_internal_value(data)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the input data to ensure it meets the necessary conditions.

        Args:
            data (Dict[str, Any]): The data to validate.

        Returns:
            Dict[str, Any]: The validated data.

        Raises:
            serializers.ValidationError: If any constraints are violated.
        """
        if data["period"] == "day" and not data.get("day"):
            raise serializers.ValidationError(
                "Day is required when the period is 'day'."
            )
        return data

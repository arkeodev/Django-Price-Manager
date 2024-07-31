import pytest
from rest_framework.exceptions import ValidationError

from dashboard_service.serializers import DashboardDataSerializer


@pytest.mark.django_db(databases=["default", "dashboard_service"])
def test_dashboard_data_serializer():
    # Valid data for period 'month'
    data_month = {
        "hotel_id": 1,
        "period": "month",
        "year": 2020,
        "month": 1,
        "booking_count": 10,
    }
    serializer = DashboardDataSerializer(data=data_month)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
    dashboard_data = serializer.save()
    assert dashboard_data.hotel_id == 1

    # Valid data for period 'day'
    data_day = {
        "hotel_id": 1,
        "period": "day",
        "year": 2020,
        "month": 1,
        "day": 1,
        "booking_count": 10,
    }
    serializer = DashboardDataSerializer(data=data_day)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
    dashboard_data = serializer.save()
    assert dashboard_data.hotel_id == 1

    # Invalid data for period 'day' without 'day' field
    invalid_data = {
        "hotel_id": 1,
        "period": "day",
        "year": 2020,
        "month": 1,
        "booking_count": 10,
    }
    serializer = DashboardDataSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "day" in serializer.errors

    # Invalid period
    invalid_period_data = data_month.copy()
    invalid_period_data["period"] = "invalid"
    serializer = DashboardDataSerializer(data=invalid_period_data)
    assert not serializer.is_valid()
    assert "period" in serializer.errors

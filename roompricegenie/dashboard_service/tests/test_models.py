import pytest
from dashboard_service.models import DashboardData


@pytest.mark.django_db(databases=["default", "dashboard_service"])
def test_dashboard_data_creation():
    dashboard_data = DashboardData.objects.create(
        hotel_id=1, period="month", year=2020, month=1, booking_count=10
    )
    assert dashboard_data.hotel_id == 1
    assert dashboard_data.booking_count == 10

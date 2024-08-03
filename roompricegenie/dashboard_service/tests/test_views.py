from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from dashboard_service.models import DashboardData


@pytest.mark.django_db(databases=["dashboard_service"])
@patch("requests.get")
def test_dashboard_view(mock_get):
    # Mock response data for GET /events
    mock_response = [
        {
            "id": 1,
            "hotel_id": 1,
            "timestamp": "2020-01-01T00:00:00Z",
            "rpg_status": 1,
            "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360",
            "night_of_stay": "2020-01-01",
        }
    ]
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    client = APIClient()
    DashboardData.objects.create(
        hotel_id=1, period="month", year=2020, month=1, booking_count=10
    )
    response = client.get(
        "/dashboard/",
        {"hotel_id": 1, "period": "month", "year": 2020},
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["booking_count"] == 10

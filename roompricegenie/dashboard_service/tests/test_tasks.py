from datetime import datetime
from unittest.mock import patch

import pytest

from dashboard_service.models import DashboardData
from dashboard_service.tasks import update_dashboard_data


@pytest.mark.django_db(databases=["dashboard_service", "data_provider"])
@patch("requests.get")
def test_update_dashboard_data(mock_get):
    current_year = datetime.now().year
    mock_response = [
        {
            "id": 1,
            "hotel_id": 1,
            "event_timestamp": f"{current_year}-01-01T00:00:00Z",
            "status": 1,
            "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360",
            "night_of_stay": f"{current_year}-01-01",
        }
    ]
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    update_dashboard_data()

    # Verify that the dashboard data was updated
    dashboard_data = DashboardData.objects.filter(
        hotel_id=1, period="day", year=current_year, month=1, day=1
    )
    assert dashboard_data.exists()
    dashboard_data = dashboard_data.first()
    assert dashboard_data.booking_count == 1

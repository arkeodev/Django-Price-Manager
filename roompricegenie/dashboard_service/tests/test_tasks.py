from datetime import datetime
from unittest.mock import patch

import pytest

from dashboard_service.models import DashboardData
from dashboard_service.tasks import update_dashboard_data


@pytest.mark.django_db(databases=["default", "dashboard_service"])
@patch("requests.get")
def test_update_dashboard_data(mock_get):
    current_year = datetime.now().year
    mock_response = [
        {
            "id": 1,
            "hotel_id": 1,
            "timestamp": f"{current_year}-01-01T00:00:00Z",
            "rpg_status": 1,
            "room_id": 1,
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

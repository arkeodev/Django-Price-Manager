import pytest
from rest_framework.test import APIClient

from data_provider.models import Event


@pytest.mark.django_db(databases=["default", "data_provider"])
def test_event_list_create_view():
    client = APIClient()
    data = {
        "hotel_id": 1,
        "timestamp": "2020-01-01T00:00:00Z",
        "rpg_status": 1,
        "room_id": 1,
        "night_of_stay": "2020-01-01",
    }
    response = client.post("/api/data_provider/events/", data, format="json")
    assert response.status_code == 201
    assert Event.objects.count() == 1

    response = client.get("/api/data_provider/events/")
    assert response.status_code == 200
    assert len(response.data) == 1

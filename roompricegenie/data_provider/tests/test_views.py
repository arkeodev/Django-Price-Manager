import pytest
from data_provider.models import Event
from rest_framework.test import APIClient


@pytest.mark.django_db(databases=["default", "data_provider"])
def test_event_list_create_view():
    client = APIClient()
    data = {
        "hotel_id": 1,
        "event_timestamp": "2020-01-01T00:00:00Z",
        "status": 1,
        "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360",
        "night_of_stay": "2020-01-01",
    }
    response = client.post("/events/", data, format="json")
    assert response.status_code == 201
    assert Event.objects.count() == 1

    response = client.get("/events/")
    assert response.status_code == 200
    assert len(response.data) == 1

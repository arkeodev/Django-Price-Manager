import pytest
from rest_framework.exceptions import ValidationError

from data_provider.serializers import EventSerializer


@pytest.mark.django_db(databases=["data_provider"])
def test_event_serializer():
    data = {
        "hotel_id": 1,
        "event_timestamp": "2020-01-01T00:00:00Z",
        "status": 1,
        "room_reservation_id": "0013e338-0158-4d5c-8698-aebe00cba360",
        "night_of_stay": "2020-01-01",
    }
    serializer = EventSerializer(data=data)
    assert serializer.is_valid()
    event = serializer.save()
    assert event.hotel_id == 1

    invalid_data = data.copy()
    invalid_data["status"] = 3  # Invalid status
    serializer = EventSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

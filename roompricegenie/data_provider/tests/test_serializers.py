import pytest
from rest_framework.exceptions import ValidationError

from data_provider.serializers import EventSerializer


@pytest.mark.django_db(databases=["default", "data_provider"])
def test_event_serializer():
    data = {
        "hotel_id": 1,
        "timestamp": "2020-01-01T00:00:00Z",
        "rpg_status": 1,
        "room_id": 1,
        "night_of_stay": "2020-01-01",
    }
    serializer = EventSerializer(data=data)
    assert serializer.is_valid()
    event = serializer.save()
    assert event.hotel_id == 1

    invalid_data = data.copy()
    invalid_data["rpg_status"] = 3  # Invalid status
    serializer = EventSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

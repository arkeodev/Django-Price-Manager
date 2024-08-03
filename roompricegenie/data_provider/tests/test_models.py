import pytest

from data_provider.models import Event


@pytest.mark.django_db(databases=["data_provider"])
def test_event_creation():
    event = Event.objects.create(
        hotel_id=1,
        timestamp="2020-01-01T00:00:00Z",
        rpg_status=1,
        room_reservation_id="0013e338-0158-4d5c-8698-aebe00cba360",
        night_of_stay="2020-01-01",
    )
    assert event.hotel_id == 1
    assert event.rpg_status == 1

import uuid

from django.db import models


class Event(models.Model):
    """
    Model representing an event in a hotel booking system.

    Attributes:
    - id: Primary key for the event.
    - hotel_id: ID of the hotel where the event occurred.
    - timestamp: Timestamp of the event.
    - rpg_status: Status of the event (1 for booking, 2 for cancellation).
    - room_id: UUID of the room associated with the event.
    - night_of_stay: Date of stay for the booking event.
    """

    BOOKING = 1
    CANCELLATION = 2
    RPG_STATUS_CHOICES = [
        (BOOKING, "Booking"),
        (CANCELLATION, "Cancellation"),
    ]

    id = models.AutoField(primary_key=True)
    hotel_id = models.IntegerField()
    timestamp = models.DateTimeField()
    rpg_status = models.IntegerField(choices=RPG_STATUS_CHOICES)
    room_id = models.UUIDField(default=uuid.uuid4)
    night_of_stay = models.DateField()

    def __str__(self) -> str:
        return f"Event {self.id} - Hotel {self.hotel_id}"

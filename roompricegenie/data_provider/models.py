"""
Module defining the Event model for the RoomPriceGenie project.

This module contains the Event model which represents events in a hotel booking system.
"""

import uuid

from django.db import models


class Event(models.Model):
    """
    A Django model that represents an event in a hotel booking system.

    Attributes:
        id (AutoField): The primary key for the event.
        hotel_id (IntegerField): The ID of the hotel where the event occurred.
        timestamp (DateTimeField): The exact date and time when the event was recorded.
        rpg_status (IntegerField): Represents the status of the event, distinguishing between booking and cancellation.
        room_reservation_id (UUIDField): The UUID of the room reservation associated with the event.
        night_of_stay (DateField): The specific date of stay associated with the event.

    Constants:
        BOOKING (int): Constant value representing a booking event.
        CANCELLATION (int): Constant value representing a cancellation event.

    Choices:
        RPG_STATUS_CHOICES (list of tuples): Defines permissible choices for the `rpg_status` field.
    """

    # Defining constants for readability and maintainability of event status
    BOOKING: int = 1
    CANCELLATION: int = 2

    # Choices for the RPG status field to ensure database integrity
    RPG_STATUS_CHOICES: list[tuple[int, str]] = [
        (BOOKING, "Booking"),
        (CANCELLATION, "Cancellation"),
    ]

    # Model fields
    id: int = models.AutoField(primary_key=True)
    hotel_id: int = models.IntegerField(
        help_text="The ID of the hotel where the event took place."
    )
    timestamp: str = models.DateTimeField(
        help_text="The date and time when the event was recorded."
    )
    rpg_status: int = models.IntegerField(
        choices=RPG_STATUS_CHOICES,
        help_text="The status of the event, either booking or cancellation.",
    )
    room_reservation_id: str = models.UUIDField(
        default=uuid.uuid4, help_text="A unique identifier for the room reservation."
    )
    night_of_stay: str = models.DateField(
        help_text="The date of stay for which the event is booked or canceled."
    )

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the model instance.

        Returns:
            str: A string describing the event, including its ID and associated hotel ID.
        """
        return f"Event {self.id} - Hotel {self.hotel_id}"

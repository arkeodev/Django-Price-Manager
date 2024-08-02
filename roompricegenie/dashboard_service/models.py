"""
Module defining the DashboardData model for the RoomPriceGenie project.

This module contains the DashboardData model which represents aggregated booking data
for hotels over different periods.
"""

from typing import Tuple

from django.db import models


class DashboardData(models.Model):
    """
    A Django model that represents aggregated booking data for hotels over different periods.

    Attributes:
        hotel_id (IntegerField): The ID of the hotel.
        period (CharField): The period of aggregation ('month' or 'day').
        year (IntegerField): The year of the data.
        month (IntegerField): The month of the data (optional if period is 'day').
        day (IntegerField): The day of the data (optional if period is 'month').
        booking_count (IntegerField): The count of bookings for the specified period.

    Meta:
        unique_together (Tuple[Tuple[str, ...], ...]): Ensures that each combination of hotel_id, year, month, day, and period is unique.
    """

    # Model fields
    hotel_id: int = models.IntegerField(help_text="The ID of the hotel.")
    period: str = models.CharField(
        max_length=10,
        choices=[("month", "Monthly"), ("day", "Daily")],
        help_text="The period of aggregation ('month' or 'day').",
    )
    year: int = models.IntegerField(help_text="The year of the data.")
    month: int = models.IntegerField(
        help_text="The month of the data (optional if period is 'day')."
    )
    day: int = models.IntegerField(
        null=True,
        blank=True,
        help_text="The day of the data (optional if period is 'month').",
    )
    booking_count: int = models.IntegerField(
        default=0, help_text="The count of bookings for the specified period."
    )

    class Meta:
        unique_together: Tuple[Tuple[str, ...], ...] = (
            ("hotel_id", "year", "month", "day", "period"),
        )
        verbose_name = "Dashboard Data"
        verbose_name_plural = "Dashboard Data"

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the model instance.

        Returns:
            str: A string describing the dashboard data, including the hotel ID and period.
        """
        return f"DashboardData for Hotel {self.hotel_id} - {self.period.capitalize()} {self.year}-{self.month or ''}-{self.day or ''}"

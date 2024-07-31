from django.db import models


class DashboardData(models.Model):
    """
    Model representing dashboard data for hotel bookings.

    Attributes:
    - id: Primary key for the dashboard data entry.
    - hotel_id: ID of the hotel.
    - period: The period of the dashboard data (e.g., 'month', 'day').
    - year: The year of the dashboard data.
    - month: The month of the dashboard data (nullable).
    - day: The day of the dashboard data (nullable).
    - booking_count: Number of bookings in the specified period.
    """

    PERIOD_CHOICES = [
        ("month", "Monthly"),
        ("day", "Daily"),
    ]

    id = models.AutoField(primary_key=True)
    hotel_id = models.IntegerField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    booking_count = models.IntegerField()

    class Meta:
        unique_together = (("hotel_id", "period", "year", "month", "day"),)

    def __str__(self) -> str:
        return f"Dashboard Data - Hotel {self.hotel_id}, Period {self.period}, Year {self.year}"

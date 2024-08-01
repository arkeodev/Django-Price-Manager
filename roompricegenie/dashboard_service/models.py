from django.db import models


class DashboardData(models.Model):
    hotel_id = models.IntegerField()
    period = models.CharField(
        max_length=10, choices=[("month", "Monthly"), ("day", "Daily")]
    )
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField(null=True, blank=True)
    booking_count = models.IntegerField(default=0)

    class Meta:
        unique_together = (("hotel_id", "year", "month", "day", "period"),)

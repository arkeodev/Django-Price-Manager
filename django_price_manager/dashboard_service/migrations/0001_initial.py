# Generated by Django 5.0.7 on 2024-08-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DashboardData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hotel_id", models.IntegerField(help_text="The ID of the hotel.")),
                (
                    "period",
                    models.CharField(
                        choices=[("month", "Monthly"), ("day", "Daily")],
                        help_text="The period of aggregation ('month' or 'day').",
                        max_length=10,
                    ),
                ),
                ("year", models.IntegerField(help_text="The year of the data.")),
                (
                    "month",
                    models.IntegerField(
                        help_text="The month of the data (optional if period is 'day')."
                    ),
                ),
                (
                    "day",
                    models.IntegerField(
                        blank=True,
                        help_text="The day of the data (optional if period is 'month').",
                        null=True,
                    ),
                ),
                (
                    "booking_count",
                    models.IntegerField(
                        default=0,
                        help_text="The count of bookings for the specified period.",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dashboard Data",
                "verbose_name_plural": "Dashboard Data",
                "unique_together": {("hotel_id", "year", "month", "day", "period")},
            },
        ),
    ]

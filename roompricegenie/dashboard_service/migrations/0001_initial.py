# Generated by Django 5.0.7 on 2024-08-01 14:12

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
                ("hotel_id", models.IntegerField()),
                (
                    "period",
                    models.CharField(
                        choices=[("month", "Monthly"), ("day", "Daily")], max_length=10
                    ),
                ),
                ("year", models.IntegerField()),
                ("month", models.IntegerField()),
                ("day", models.IntegerField(blank=True, null=True)),
                ("booking_count", models.IntegerField(default=0)),
            ],
            options={
                "unique_together": {("hotel_id", "year", "month", "day", "period")},
            },
        ),
    ]

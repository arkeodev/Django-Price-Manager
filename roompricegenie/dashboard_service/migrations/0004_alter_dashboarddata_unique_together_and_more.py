# Generated by Django 5.0.7 on 2024-07-31 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard_service", "0003_remove_dashboarddata_cancellation_count"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="dashboarddata",
            unique_together={("hotel_id", "year", "month", "day", "period")},
        ),
        migrations.AlterField(
            model_name="dashboarddata",
            name="booking_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="dashboarddata",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]

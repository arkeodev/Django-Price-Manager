# Generated by Django 5.0.7 on 2024-07-31 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard_service", "0002_dashboarddata_cancellation_count_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dashboarddata",
            name="cancellation_count",
        ),
    ]

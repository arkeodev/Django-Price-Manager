import logging
from datetime import datetime, timedelta

import requests
from celery import shared_task

from .models import DashboardData

logger = logging.getLogger("dashboard_service")


@shared_task
def update_dashboard_data():
    """
    Periodic task to update the dashboard data.
    """
    try:
        yesterday = datetime.now() - timedelta(days=1)
        response = requests.get(
            "http://localhost:8000/events/",
            params={"from_timestamp": yesterday.isoformat()},
        )
        response.raise_for_status()
        events = response.json()

        for event in events:
            DashboardData.objects.update_or_create(
                hotel_id=event["hotel_id"],
                period="day",
                year=int(event["timestamp"][:4]),
                month=int(event["timestamp"][5:7]),
                day=int(event["timestamp"][8:10]),
                defaults={"booking_count": 1 if event["rpg_status"] == 1 else 0},
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to GET events: {e}")

import logging
import os
from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import get_current_timezone, make_aware

from data_provider.models import Event

from .models import DashboardData

logger = logging.getLogger("dashboard_service")


def get_initial_timestamp():
    """
    Retrieve the earliest timestamp or a default if none exists, using cache to optimize.
    """
    try:
        initial_timestamp = cache.get("last_processed_timestamp")
        if initial_timestamp is None:
            earliest_event = Event.objects.order_by("timestamp").first()
            if earliest_event:
                initial_timestamp = earliest_event.timestamp.isoformat()
                logger.info(f"Earliest event timestamp found: {initial_timestamp}")
            else:
                initial_timestamp = datetime(2020, 1, 1).isoformat()
                logger.info(
                    "No events found, setting initial timestamp to the start of 2020."
                )
            cache.set("last_processed_timestamp", initial_timestamp, timeout=None)
        return initial_timestamp
    except Exception as e:
        logger.error(f"Failed to retrieve initial timestamp: {str(e)}")
        return datetime(2020, 1, 1).isoformat()  # Fallback timestamp


@shared_task
def update_dashboard_data():
    """
    Update or create daily and monthly dashboard entries from new events.
    """
    try:
        base_url = os.getenv(
            "EVENTS_API_BASE_URL", "http://127.0.0.1:8000/api/data_provider"
        )
        last_timestamp = get_initial_timestamp()
        logger.info(f"Fetching events from {last_timestamp}")

        response = requests.get(
            f"{base_url}/events/", params={"from_timestamp": last_timestamp}
        )
        if response.status_code == 200:
            events = response.json()
            logger.info(f"Received {len(events)} events from the API")

            new_last_timestamp = last_timestamp
            for event in events:
                try:
                    date = make_aware(
                        datetime.strptime(
                            event["event_timestamp"], "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        timezone=get_current_timezone(),
                    )
                    update_dashboard(date, event, "day")
                    update_dashboard(date, event, "month")
                    new_last_timestamp = max(
                        new_last_timestamp, event["event_timestamp"]
                    )
                except Exception as e:
                    logger.error(f"Error processing event {event['id']}: {str(e)}")
                    continue

            cache.set("last_processed_timestamp", new_last_timestamp)
            logger.info(f"Dashboard updated up to {new_last_timestamp}")
        else:
            logger.error(
                f"Failed to fetch events: {response.status_code} - {response.text}"
            )
    except Exception as e:
        logger.error(f"Unhandled error in update_dashboard_data: {str(e)}")


def update_dashboard(date, event, period):
    """
    Helper function to update or create dashboard data for a given period.
    """
    try:
        filter_kwargs = {
            "hotel_id": event["hotel_id"],
            "year": date.year,
            "period": period,
            "month": date.month,
            "day": date.day if period == "day" else None,
        }
        current_count = (
            DashboardData.objects.filter(**filter_kwargs).aggregate(
                total=Sum("booking_count")
            )["total"]
            or 0
        )
        updated_count = current_count + (1 if event.get("status", 1) == 1 else -1)

        _, created = DashboardData.objects.update_or_create(
            defaults={"booking_count": updated_count}, **filter_kwargs
        )
        record_type = "created" if created else "updated"
        logger.info(
            f"{record_type.capitalize()} {period} record for {filter_kwargs} with updated count {updated_count}"
        )
    except Exception as e:
        logger.error(f"Error updating dashboard for {filter_kwargs}: {str(e)}")

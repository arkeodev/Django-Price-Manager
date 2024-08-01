import logging
from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import make_aware

from data_provider.models import Event

from .models import DashboardData

logger = logging.getLogger("data_provider")


def get_initial_timestamp():
    """
    Retrieve the earliest timestamp or a default if none exists, using cache to optimize.
    """
    initial_timestamp = cache.get("last_processed_timestamp")
    if initial_timestamp is None:
        try:
            earliest_event = Event.objects.order_by("timestamp").first()
            initial_timestamp = (
                earliest_event.timestamp.isoformat()
                if earliest_event
                else datetime(2020, 1, 1).isoformat()
            )
            cache.set("last_processed_timestamp", initial_timestamp, timeout=None)
            logger.info(f"Initial timestamp set to {initial_timestamp}")
        except Exception as e:
            logger.error(f"Error fetching initial timestamp: {str(e)}")
            initial_timestamp = datetime.now().isoformat()
            cache.set("last_processed_timestamp", initial_timestamp)
    return initial_timestamp


@shared_task
def update_dashboard_data():
    """
    Update or create daily and monthly dashboard entries from new events.
    """
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
        logger.info(f"Received {len(events)} events")
        new_last_timestamp = last_timestamp

        for event in events:
            date = make_aware(
                datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            )
            logger.info(f"Processing event {event['id']} for date {date}")

            # Update daily data
            update_dashboard(date, event, "day")

            # Update monthly data
            update_dashboard(date, event, "month")

            # Update the last processed timestamp
            if date.isoformat() > new_last_timestamp:
                new_last_timestamp = date.isoformat()

        cache.set("last_processed_timestamp", new_last_timestamp)
        logger.info(f"Dashboard updated up to {new_last_timestamp}")
    else:
        logger.error(
            f"Failed to fetch events: {response.status_code} - {response.text}"
        )


def update_dashboard(date, event, period):
    """
    Helper function to update or create dashboard data for a given period.
    """
    filter_kwargs = {"hotel_id": event["hotel_id"], "year": date.year, "period": period}

    if period == "day":
        filter_kwargs.update({"month": date.month, "day": date.day})
    elif period == "month":
        filter_kwargs.update({"month": date.month, "day": None})

    # Aggregate current bookings
    existing_record = DashboardData.objects.filter(**filter_kwargs)
    current_count = existing_record.aggregate(total=Sum("booking_count"))["total"] or 0
    updated_count = current_count + (1 if event["rpg_status"] == 1 else -1)

    # Create or update the record
    _, created = DashboardData.objects.update_or_create(
        defaults={"booking_count": updated_count}, **filter_kwargs
    )
    record_type = "created" if created else "updated"
    logger.info(
        f"{record_type.capitalize()} {period} record for hotel_id={event['hotel_id']} on {date.date()} with count {updated_count}"
    )

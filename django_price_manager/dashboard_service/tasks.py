"""
Module for updating dashboard data using Celery.

This module defines tasks and helper functions to update or create daily and monthly
dashboard entries from new events fetched via an API.
"""

import logging
import os
from datetime import datetime

import requests
from celery import shared_task
from data_provider.models import Event
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import get_current_timezone, make_aware

from .models import DashboardData

logger = logging.getLogger(__name__)


def get_latest_timestamp():
    """
    Retrieve the latest timestamp from the cache or use a fallback.
    """
    return cache.get("last_event_timestamp") or datetime(2020, 1, 1).isoformat()


@shared_task()
def update_dashboard_data() -> None:
    """
    Update or create daily and monthly dashboard entries from new events.

    This task fetches new events from the API based on the last processed timestamp,
    processes each event, and updates the dashboard data accordingly.
    """
    try:
        logger.info("Updating dashboard data...")
        base_url = os.getenv("EVENTS_API_BASE_URL", "http://127.0.0.1:8000")
        last_timestamp = get_latest_timestamp()
        new_last_timestamp = last_timestamp  # Initialize new_last_timestamp here
        logger.info(f"Fetching events from {last_timestamp}")

        params = {"updated_gt": last_timestamp}
        response = requests.get(f"{base_url}/events/", params=params)
        if response.status_code == 200:
            events = response.json()
            logger.info(f"Received {len(events)} events from the API")

            if events:
                latest_timestamp = max(event["event_timestamp"] for event in events)
                cache.set("last_event_timestamp", latest_timestamp)
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
                        logger.debug(f"Dashboard updated for {date}")
                        new_last_timestamp = max(
                            new_last_timestamp, event["event_timestamp"]
                        )
                    except Exception as e:
                        logger.error(f"Error processing event {event['id']}: {str(e)}")
                        continue
                else:
                    logger.info("No events to process")
                logger.info(f"New timestamp is: {new_last_timestamp}")
        else:
            logger.error(
                f"Failed to fetch events: {response.status_code} - {response.text}"
            )
    except Exception as e:
        logger.error(f"Unhandled error in update_dashboard_data: {str(e)}")


def update_dashboard(date: datetime, event: dict, period: str) -> None:
    """
    Helper function to update or create dashboard data for a given period.

    Args:
        date (datetime): The date of the event.
        event (dict): The event data.
        period (str): The period to update ("day" or "month").
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

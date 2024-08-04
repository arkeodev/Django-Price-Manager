"""
This module implements functionality to load event data from a CSV file into a Redis queue. It handles the validation
of UUIDs in the data, segregates valid and invalid records, and facilitates the enqueuing of validated events for
further processing. The module integrates with Django's command infrastructure to allow manual triggering of the
event loading process through management commands. It is designed to work with Celery for task scheduling and Redis
for queue management.
"""

import json
import logging
import os
import uuid

import pandas as pd
import redis
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Configure logger
logger = logging.getLogger("roompricegenie")

# Constants for file paths
DATA_FILE_PATH: str = os.path.join(os.path.dirname(__file__), "data", "data.csv")

# Configure Redis connection
r = redis.Redis.from_url(settings.CELERY_BROKER_URL)
queue_key = "event_queue"


def is_valid_uuid(value: str) -> bool:
    """
    Validate whether the provided string is a valid UUID.

    Args:
        value (str): The string to be validated.

    Returns:
        bool: True if the string is a valid UUID, otherwise False.
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


class Command(BaseCommand):
    """
    Django management command to trigger the loading of events into a Redis queue.
    """

    help = "Triggers the load_events_to_queue Celery task"

    def handle(self, *args, **options) -> None:
        """
        Executes the management command which triggers the Celery task to load events.
        """
        try:
            load_events_to_queue()
            self.stdout.write(
                self.style.SUCCESS("Successfully triggered load_events_to_queue")
            )
        except Exception as e:
            raise CommandError(f"Error triggering task: {e}")


def load_events_to_queue() -> None:
    """
    Load events from a CSV file, validate UUIDs, and enqueue valid events for processing.
    It also logs and saves any invalid rows to a separate CSV file for further investigation.
    """
    data = pd.read_csv(DATA_FILE_PATH)
    logger.info(f"Read {len(data)} rows from CSV file.")

    # Apply UUID validation and separate valid from invalid data
    data["is_valid_uuid"] = data["room_reservation_id"].apply(is_valid_uuid)
    valid_data = data[data["is_valid_uuid"]].copy()
    invalid_rows = data[~data["is_valid_uuid"]].copy()

    # Sort valid data by event timestamp in ascending order
    valid_data.sort_values(by="event_timestamp", ascending=True, inplace=True)

    # Log and save invalid rows if present
    if not invalid_rows.empty:
        invalid_csv_file_path = os.path.join(
            os.path.dirname(__file__), "data", "invalid_rows.csv"
        )
        invalid_rows.to_csv(invalid_csv_file_path, index=False)
        logger.info(
            f"Logged {len(invalid_rows)} invalid rows with invalid UUIDs to {invalid_csv_file_path}"
        )

    logger.info(f"Filtered data to {len(valid_data)} rows with valid UUIDs.")

    # Enqueue valid events into the Redis queue
    for _, row in valid_data.iterrows():
        r.rpush(queue_key, json.dumps(row.to_dict()))
    logger.info(f"Enqueued {len(valid_data)} events to Redis.")

import json
import logging
import os
import uuid

import pandas as pd
import redis
import requests
from celery import shared_task
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger("roompricegenie")

# Constants for file paths
DATA_FILE_PATH: str = os.path.join(os.path.dirname(__file__), "data", "data.csv")


def is_valid_uuid(value: str) -> bool:
    """
    Validate whether a given string is a valid UUID.

    Args:
        value (str): The string to validate as UUID.

    Returns:
        bool: True if the string is a valid UUID, False otherwise.
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


r = redis.Redis(host="127.0.0.1", port=6379, db=0)  # Configure as needed
queue_key = "event_queue"


class Command(BaseCommand):
    help = "Triggers the load_events_to_queue Celery task"

    def handle(self, *args, **options):
        try:
            load_events_to_queue()
            self.stdout.write(
                self.style.SUCCESS("Successfully triggered load_events_to_queue")
            )
        except Exception as e:
            raise CommandError(f"Error triggering task: {e}")


def load_events_to_queue():
    """
    Task to load events from a CSV file, validate the UUIDs, and enqueue them for processing.
    Invalid rows are saved to a separate CSV file.
    """

    data = pd.read_csv(DATA_FILE_PATH)
    logger.info(f"Read {len(data)} rows from CSV file.")

    # Apply UUID validation and store results in a new column
    data["is_valid_uuid"] = data["room_reservation_id"].apply(is_valid_uuid)

    # Separate valid and invalid data based on the new column
    valid_data = data[data["is_valid_uuid"]].copy()
    invalid_rows = data[~data["is_valid_uuid"]].copy()

    # Sort data by the event timestamp in ascending order
    valid_data.sort_values(by="event_timestamp", ascending=True, inplace=True)

    # Log and save invalid rows to a CSV file if any exist
    if not invalid_rows.empty:
        invalid_csv_file_path = os.path.join(
            os.path.dirname(__file__), "data", "invalid_rows.csv"
        )
        invalid_rows.to_csv(invalid_csv_file_path, index=False)
        logger.info(
            f"Logged {len(invalid_rows)} invalid rows with invalid UUIDs to {invalid_csv_file_path}"
        )

    logger.info(f"Filtered data to {len(valid_data)} rows with valid UUIDs.")

    # Push each valid event into the Redis queue
    for _, row in valid_data.iterrows():
        r.rpush(queue_key, json.dumps(row.to_dict()))
    logger.info(f"Enqueued {len(valid_data)} events to Redis.")

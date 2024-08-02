"""
Module for simulating event creation using Celery.

This module defines a periodic task to simulate the creation of booking and cancellation
events from CSV data. Events are sent to an API in chronological order.
"""

import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from celery import shared_task
from django.conf import settings

logger = logging.getLogger("data_provider")

# Path to the CSV file containing event data
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "data.csv")


@shared_task
def simulate_event_creation() -> None:
    """
    Periodic task to simulate the creation of booking and cancellation events from CSV data,
    ensuring events are sent in chronological order.

    This task reads event data from a CSV file, processes each row, and sends a POST request
    to the events API endpoint. Invalid rows are logged and saved to a separate CSV file.
    """
    base_url = os.getenv("EVENTS_API_BASE_URL", "http://127.0.0.1:8000")
    if not base_url:
        logger.error("EVENTS_API_BASE_URL is not configured.")
        raise ValueError("EVENTS_API_BASE_URL is not set")

    try:
        # Read the CSV file
        data = pd.read_csv(DATA_FILE_PATH)
        logger.info(f"The number of rows in the CSV data: {len(data)}")

        # Sort data by the event timestamp in ascending order
        data.sort_values(by="event_timestamp", ascending=True, inplace=True)

        # Lists to track invalid rows and count invalid UUIDs
        invalid_rows: List[Dict[str, Any]] = []
        invalid_uuid_count = 0

        # Iterate over each row in the data
        for index, row in data.iterrows():
            try:
                event_data = row.to_dict()
                logger.debug(f"Posting event: {event_data}")

                # Send POST request to the events API
                response = requests.post(f"{base_url}/events/", json=event_data)
                response.raise_for_status()

                logger.debug(f"Successfully posted event ID: {row['id']}")
            except requests.exceptions.HTTPError as e:
                logger.error(
                    f"HTTP error for event {row['id']}: {str(e)} - Status Code: {response.status_code}"
                )
                invalid_rows.append(row)
                invalid_uuid_count += 1
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for event {row['id']}: {str(e)}")
                invalid_rows.append(row)
                invalid_uuid_count += 1

        # Save invalid rows to a CSV file
        if invalid_rows:
            invalid_csv_file_path = os.path.join(
                os.path.dirname(__file__), "data", "invalid_rows.csv"
            )
            pd.DataFrame(invalid_rows).to_csv(invalid_csv_file_path, index=False)
            logger.info(
                f"Logged {len(invalid_rows)} invalid rows to {invalid_csv_file_path}"
            )

    except Exception as e:
        logger.error(f"Unexpected error while simulating event creation: {str(e)}")

import logging
import os

import pandas as pd
import requests
from celery import shared_task
from django.conf import settings

logger = logging.getLogger("data_provider")

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "data_1.csv")


@shared_task
def simulate_event_creation():
    """
    Periodic task to simulate the creation of booking and cancellation events from CSV data,
    ensuring events are sent in chronological order.
    """
    base_url = os.getenv(
        "EVENTS_API_BASE_URL", "http://127.0.0.1:8000/api/data_provider"
    )
    if not base_url:
        logger.error("EVENTS_API_BASE_URL is not configured.")
        raise ValueError("EVENTS_API_BASE_URL is not set")

    try:
        data = pd.read_csv(DATA_FILE_PATH)
        logging.info(f"The number of rows in the CSV data: {len(data)}")
        data.sort_values(by="event_timestamp", ascending=True, inplace=True)

        invalid_rows = []
        invalid_uuid_count = 0

        for index, row in data.iterrows():
            try:
                event_data = row.to_dict()
                logger.debug(f"Posting event: {event_data}")
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

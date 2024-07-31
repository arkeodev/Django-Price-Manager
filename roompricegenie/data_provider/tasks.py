import logging
import os

import pandas as pd
import requests
from celery import shared_task

logger = logging.getLogger("data_provider")

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "data.csv")


@shared_task
def simulate_event_creation():
    """
    Periodic task to simulate the creation of booking and cancellation events from CSV data.
    """
    data = pd.read_csv(DATA_FILE_PATH)
    invalid_rows = []
    invalid_uuid_count = 0

    for index, row in data.iterrows():
        try:
            response = requests.post(
                "http://localhost:8000/events/", json=row.to_dict()
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to POST event: {row['id']} - {e}")
            invalid_rows.append(row)
            invalid_uuid_count += 1
            continue

    if invalid_rows:
        invalid_csv_file_path = os.path.join(
            os.path.dirname(__file__), "data", "invalid_rows.csv"
        )
        invalid_df = pd.DataFrame(invalid_rows)
        invalid_df.to_csv(invalid_csv_file_path, index=False)
        logger.debug(
            f"Logged {len(invalid_rows)} invalid rows to {invalid_csv_file_path}"
        )

    if invalid_uuid_count > 0:
        logger.info(
            f"{invalid_uuid_count} invalid UUID items found in the data file and logged to {invalid_csv_file_path}"
        )

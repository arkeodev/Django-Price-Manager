"""
Module for simulating event creation from CSV data using Celery and Redis.

This module defines a periodic Celery task that simulates the creation of booking and
cancellation events from CSV data, ensuring events are sent in chronological order.
It uses Redis via Django's caching framework to track the last processed record
to avoid reprocessing data on subsequent runs.
"""

import json
import logging
import os

import redis
import requests
from celery import shared_task

logger = logging.getLogger("roompricegenie")

r = redis.Redis(host="127.0.0.1", port=6379, db=0)  # Configure as needed
queue_key = "event_queue"


@shared_task
def process_event_from_queue():
    """
    Dequeue events from Redis and process them by posting to the data_provider database.
    """
    while True:
        # Non-blocking pop from Redis queue
        logger.info("Reading event from Redis...")
        event_data_json = r.lpop(queue_key)
        logger.info(f"Event data: {event_data_json}")
        if event_data_json is None:
            break

        event_data = json.loads(event_data_json)
        try:
            base_url = os.getenv("EVENTS_API_BASE_URL", "http://127.0.0.1:8000")
            response = requests.post(f"{base_url}/events/", json=event_data)
            response.raise_for_status()
            logger.info(f"Event {event_data.get('id', 'Unknown')} successfully posted.")
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Failed to post event {event_data.get('id', 'Unknown')}: {str(e)}"
            )

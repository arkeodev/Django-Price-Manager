from __future__ import absolute_import, unicode_literals

import os
from typing import Any

from celery import Celery
from celery.schedules import schedule

# Setting the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roompricegenie.settings")

# Create a new Celery instance and configure it using the settings from Django.
app = Celery("roompricegenie")

# Load configuration from the Django settings, specifying the namespace 'CELERY'.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django app configs.
app.autodiscover_tasks()

# Define periodic tasks using the beat scheduler.
app.conf.beat_schedule = {
    "simulate-event-creation-every-5-seconds": {
        "task": "data_provider.tasks.simulate_event_creation",
        "schedule": schedule(5.0),  # Run every 5 seconds.
    },
    "update-dashboard-data-every-20-seconds": {
        "task": "dashboard_service.tasks.update_dashboard_data",
        "schedule": schedule(20.0),  # Run every 20 seconds.
    },
}


@app.task(bind=True)
def debug_task(self: Any) -> None:
    """
    A debug task that prints the current request. This can be useful for debugging.
    """
    print(f"Request: {self.request!r}")

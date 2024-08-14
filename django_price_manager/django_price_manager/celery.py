"""
Celery configuration module for the Django Price Manager project.

This module sets up Celery, a distributed task queue, with the settings and tasks defined
for the project.
"""

from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_price_manager.settings")

app = Celery("django_price_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Define custom task routing
app.conf.task_routes = {
    "dashboard_service.tasks.*": {"queue": "dashboard_queue"},
}

app.autodiscover_tasks()

# Define periodic tasks using the beat scheduler.
app.conf.beat_schedule = {
    "update-dashboard-data-from-events": {
        "task": "dashboard_service.tasks.update_dashboard_data",
        "schedule": timedelta(seconds=5),  # Run every 5 seconds
        "options": {"queue": "dashboard_queue"},
    },
    "process-event-from-queue": {
        "task": "data_provider.tasks.process_event_from_queue",
        "schedule": timedelta(seconds=5),  # Run every 5 seconds
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

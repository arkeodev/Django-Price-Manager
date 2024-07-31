from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import schedule

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roompricegenie.settings")

app = Celery("roompricegenie")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "simulate-event-creation-every-1-minute": {
        "task": "data_provider.tasks.simulate_event_creation",
        "schedule": schedule(60.0),  # Every 1 minute
    },
    "update-dashboard-data-every-1-minute": {
        "task": "dashboard_service.tasks.update_dashboard_data",
        "schedule": schedule(60.0),  # Every 1 minute
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

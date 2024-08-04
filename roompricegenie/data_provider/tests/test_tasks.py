import json
import os
from unittest.mock import MagicMock, patch

import pytest
from data_provider.tasks import process_event


@pytest.mark.django_db(databases=["data_provider"])
@patch("requests.post")
@patch("redis.Redis.lpop")
def test_process_event_from_queue(mock_redis_lpop, mock_post):
    event_data_json = json.dumps(
        {"id": "1234", "event_timestamp": "2021-08-01T00:00:00Z"}
    )
    mock_post.return_value = MagicMock(status_code=201)
    mock_post.return_value.raise_for_status = MagicMock()

    # When
    process_event(event_data_json)

    base_url = os.getenv("EVENTS_API_BASE_URL", "http://127.0.0.1:8000") + "/events/"
    # Check if requests.post was called with the correct URL and data
    mock_post.assert_called_once_with(
        base_url, json={"id": "1234", "event_timestamp": "2021-08-01T00:00:00Z"}
    )

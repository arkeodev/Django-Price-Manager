from unittest.mock import patch

import pytest
import requests
from data_provider.tasks import simulate_event_creation


@pytest.mark.django_db(databases=["default", "data_provider"])
@patch("requests.post")
def test_simulate_event_creation(mock_post):
    mock_post.return_value.status_code = 201

    simulate_event_creation()

    # Check for logging or any other assertions related to your task
    # This depends on what exactly you want to assert in your task
    assert mock_post.called

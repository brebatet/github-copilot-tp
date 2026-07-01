from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Keep in-memory activity data isolated across tests."""
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

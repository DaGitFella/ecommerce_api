import pytest
from fastapi.testclient import TestClient

from ecommerce_api.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ecommerce_api.infrastructure.database import table_registry
from ecommerce_api.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(bind=engine)

    with Session(engine) as SessionLocal:
        yield SessionLocal

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(model, timestamp=datetime(2024, 1, 1)):
    """Helper function to mock the created_at field for testing."""

    def set_timestamp(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = timestamp

    event.listen(model, 'before_insert', set_timestamp)

    yield timestamp

    event.remove(model, 'before_insert', set_timestamp)


@pytest.fixture
def mock_db_time():
    return _mock_db_time

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ecommerce_api.infrastructure.database import table_registry
from ecommerce_api.main import app
from ecommerce_api.models.users import User
from ecommerce_api.schemas.product_schema import CreateProduct
from ecommerce_api.schemas.user_schema import UserCreate
from ecommerce_api.services.product_service import ProductService
from ecommerce_api.services.user_services import UserService
from tests.fakes.fake_product_repo import FakeProductRepo
from tests.fakes.fake_user_repo import FakeUserRepo


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


@pytest.fixture
def user(session) -> User:
    user = User(email='test@test.com', name='test', password_hash='test123')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def user_two(session) -> User:
    user = User(email='alice@example.com', name='alice', password_hash='alicepassword')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def user_service():
    return UserService(FakeUserRepo())


@pytest.fixture
def user_repo():
    return FakeUserRepo()


@pytest.fixture
def fake_repo_with_users():
    repo = FakeUserRepo()

    user = UserCreate(email='taken@email.com', name='taken', password='alicepassword')

    user_two = UserCreate(email='email@example.com', name='usuario', password='secret')

    repo.create_user(data=user)
    repo.create_user(data=user_two)

    return repo


@pytest.fixture
def user_service_with_users(fake_repo_with_users):
    return UserService(fake_repo_with_users)


@pytest.fixture
def fake_repo_with_products():
    repo = FakeProductRepo()

    product = CreateProduct(
        name='maquina legal',
        description='maquina de alta tração incrivel',
        price=999,
        stock=5,
    )

    product_two = CreateProduct(
        name='Máquina épica', description='Máquina de baixa tração', price=5, stock=999
    )

    repo.create_product(product)
    repo.create_product(product_two)

    return repo


@pytest.fixture
def fake_product_service():
    return ProductService(FakeProductRepo())


@pytest.fixture
def fake_product_service_with_products(fake_repo_with_products):
    return ProductService(fake_repo_with_products)

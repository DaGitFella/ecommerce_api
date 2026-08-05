from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ecommerce_api.domains.categories.schema import CategoryCreate
from ecommerce_api.domains.categories.service import CategoryService
from ecommerce_api.domains.products.schema import ProductCreate
from ecommerce_api.domains.products.service import ProductService
from ecommerce_api.domains.shopping_carts.service import ShoppingCartService
from ecommerce_api.domains.users.models import User
from ecommerce_api.domains.users.schema import UserCreate
from ecommerce_api.domains.users.service import UserService
from ecommerce_api.infrastructure.database import table_registry
from ecommerce_api.main import app
from tests.fakes.events.fake_event_bus import FakeEventBus
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.repositories.fake_category_repo import FakeCategoryRepo
from tests.fakes.repositories.fake_product_repo import FakeProductRepo
from tests.fakes.repositories.fake_shopping_cart_repo import FakeShoppingCartRepo
from tests.fakes.repositories.fake_user_repo import FakeUserRepo


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
    return UserService(
        FakeUserRepo(), password_hash=FakePasswordHasher(), event_bus=FakeEventBus()
    )


@pytest.fixture
async def fake_user_service_with_users():
    bus = FakeEventBus()
    repo = FakeUserRepo()

    service = UserService(repo, password_hash=FakePasswordHasher(), event_bus=bus)

    user = UserCreate(email='taken@email.com', name='taken', password='alicepassword')

    user_two = UserCreate(email='email@example.com', name='usuario', password='secret')

    user_three = UserCreate(
        email='deactive@example.com', name='deactivated', password='hard password'
    )

    await service.register(user)
    await service.register(user_two)
    deactivated_user = await service.register(user_three)

    service.deactivate_user(deactivated_user.id)

    return service


@pytest.fixture
async def fake_shopping_cart_service():
    service = ShoppingCartService(FakeShoppingCartRepo())

    test_user = User(
        email='test@example.com',
        password_hash='pedro.hashed.password.test',
        name='hoberval',
    )

    test_user.id = 1

    await service.create_default_shopping_cart(user=test_user)

    return service


@pytest.fixture
async def fake_category_service_with_categories():
    repo = FakeCategoryRepo()
    service = CategoryService(repo)

    category = CategoryCreate(name='Electronics', slug='electronics')
    category_two = CategoryCreate(name='Books', slug='books')

    await service.get_or_create_category(category)
    await service.get_or_create_category(category_two)

    return service


@pytest.fixture
def fake_category_service():
    return CategoryService(FakeCategoryRepo())


@pytest.fixture
def fake_repo_with_products():
    repo = FakeProductRepo()

    product = ProductCreate(
        name='maquina legal',
        description='maquina de alta tração incrivel',
        price=999,
        stock=5,
    )

    product_two = ProductCreate(
        name='Máquina épica', description='Máquina de baixa tração', price=5, stock=999
    )

    repo.create_product(product)
    repo.create_product(product_two)

    return repo


@pytest.fixture
def fake_product_service():
    return ProductService(repo=FakeProductRepo(), event_bus=FakeEventBus())


@pytest.fixture
def fake_product_service_with_products(fake_repo_with_products):
    return ProductService(
        repo=fake_repo_with_products,
        event_bus=FakeEventBus(),
    )

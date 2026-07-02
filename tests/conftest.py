from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ecommerce_api.categories.schema import CategoryCreate
from ecommerce_api.categories.service import CategoryService
from ecommerce_api.infrastructure.database import table_registry
from ecommerce_api.main import app
from ecommerce_api.products.schema import ProductCreate
from ecommerce_api.products.service import ProductService
from ecommerce_api.shopping_carts.service import ShoppingCartService
from ecommerce_api.users.models import User
from ecommerce_api.users.schema import UserCreate
from ecommerce_api.users.service import UserService
from tests.fakes.fake_category_repo import FakeCategoryRepo
from tests.fakes.fake_product_repo import FakeProductRepo
from tests.fakes.fake_shopping_cart_repo import FakeShoppingCartRepo
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
    return UserService(FakeUserRepo(), ShoppingCartService(FakeProductRepo()))


@pytest.fixture
def fake_user_service_with_users():
    repo = FakeUserRepo()
    service = UserService(repo, ShoppingCartService(FakeShoppingCartRepo()))

    user = UserCreate(email='taken@email.com', name='taken', password='alicepassword')

    user_two = UserCreate(email='email@example.com', name='usuario', password='secret')

    service.register(user)
    service.register(user_two)

    return service


@pytest.fixture
def fake_repo_with_categories():
    repo = FakeCategoryRepo()

    category = CategoryCreate(name='Electronics', slug='electronics')
    category_two = CategoryCreate(name='Books', slug='books')

    repo.create(**category.model_dump())
    repo.create(**category_two.model_dump())

    return repo


@pytest.fixture
def fake_category_service_with_categories(fake_repo_with_categories):
    return CategoryService(fake_repo_with_categories)


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
    return ProductService(
        repo=FakeProductRepo(), category_service=CategoryService(FakeCategoryRepo())
    )


@pytest.fixture
def fake_product_service_with_products(fake_repo_with_products):
    return ProductService(
        repo=fake_repo_with_products,
        category_service=CategoryService(FakeCategoryRepo()),
    )

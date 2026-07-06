import pytest

from ecommerce_api.core.bootstrap import EventRegistry
from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.categories.handlers import CategoryEventHandlers
from ecommerce_api.domains.categories.schema import CategoryCreate
from ecommerce_api.domains.products.events import ProductCreated
from ecommerce_api.domains.products.models import Product
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.users.events import UserRegistered
from ecommerce_api.domains.users.models import User
from tests.fakes.services.fake_category_service import FakeCategoryService
from tests.fakes.services.fake_shopping_cart_service import FakeCartService


@pytest.mark.asyncio
async def test_subscribed_handler_is_called_on_publish():
    bus = EventBus()
    received: list[UserRegistered] = []

    async def fake_handler(event: UserRegistered) -> None:
        received.append(event)

    bus.subscribe(UserRegistered, fake_handler)

    event = UserRegistered(user=..., email='test@example.com')
    await bus.publish(event)

    assert received == [event]


@pytest.mark.asyncio
async def test_user_registered_triggers_cart_creation():
    bus = EventBus()
    event_register = EventRegistry(bus)

    cart_service = FakeCartService()  # records calls instead of hitting a DB
    cart_handlers = CartEventHandlers(cart_service=cart_service)

    event_register.register_all(cart_handlers)

    test_user = User(
        email='test@example.com',
        name='aldemir',
        password_hash='password.hash.very.hard',
    )

    event = UserRegistered(user=test_user, email=test_user.email)
    await bus.publish(event)

    assert cart_service.calls == [event.user]


@pytest.mark.asyncio
async def test_product_created_triggers_categories_creation():
    bus = EventBus()
    event_register = EventRegistry(bus)

    category_service = FakeCategoryService()
    category_handlers = CategoryEventHandlers(category_service=category_service)

    event_register.register_all(category_handlers)

    test_category = CategoryCreate(name='Eletronicos', slug='eletronics')

    test_product = Product(
        name='test', price=2.99, strock=6, categories=[test_category]
    )

    event = ProductCreated(categories=test_product.categories)
    await bus.publish(event)

    assert category_service.calls[1] == event.categories

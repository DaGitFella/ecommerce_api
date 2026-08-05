import pytest

from ecommerce_api.core.bootstrap import EventRegistry
from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.categories.handlers import CategoryEventHandlers
from ecommerce_api.domains.categories.models import Category
from ecommerce_api.domains.products.events import ProductCreated
from ecommerce_api.domains.products.models import Product
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.specifications.handlers import SpecificationsEventHandlers
from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.users.events import UserRegistered
from ecommerce_api.domains.users.models import User
from tests.fakes.services.fake_category_service import FakeCategoryService
from tests.fakes.services.fake_shopping_cart_service import FakeCartService
from tests.fakes.services.fake_specification_service import FakeSpecificationsService


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

    event_register.register_cart_handler(cart_handlers)

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

    event_register.register_category_handler(category_handlers)

    test_category = Category(name='Eletronicos', slug='eletronics')

    test_product = Product(name='test', price=2.99, stock=6, categories=[test_category])

    event = ProductCreated(categories=test_product.categories, product=test_product)

    await bus.publish(event)

    assert category_service.calls[0] == event.categories[0]


@pytest.mark.asyncio
async def test_product_created_triggers_specifications_creation():
    bus = EventBus()
    event_register = EventRegistry(bus)

    specifications_service = FakeSpecificationsService()
    specifications_handlers = SpecificationsEventHandlers(
        specification_service=specifications_service
    )

    event_register.register_specifications_handler(specifications_handlers)

    test_specification = SpecificationKey(name='Cor')

    test_product = Product(
        name='test', price=2.99, stock=6, specification_keys=[test_specification]
    )

    event = ProductCreated(
        specifications=test_product.specification_keys, product=test_product
    )

    await bus.publish(event)

    assert specifications_service.calls[0] == event.specifications[0]

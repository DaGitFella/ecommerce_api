import pytest

from ecommerce_api.core.bootstrap import register_event_handlers
from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.users.events import UserRegistered
from ecommerce_api.domains.users.models import User
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

    cart_service = FakeCartService()  # records calls instead of hitting a DB
    cart_handlers = CartEventHandlers(cart_service=cart_service)

    register_event_handlers(bus, cart_handlers)

    test_user = User(
        email='test@example.com',
        name='aldemir',
        password_hash='password.hash.very.hard',
    )

    event = UserRegistered(user=test_user, email=test_user.email)
    await bus.publish(event)

    assert cart_service.calls == [event.user]

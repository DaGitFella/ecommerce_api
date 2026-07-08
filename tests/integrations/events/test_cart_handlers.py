import pytest

from ecommerce_api.core.bootstrap import EventRegistry
from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.shopping_carts.service import ShoppingCartService
from ecommerce_api.domains.users.schema import UserCreate
from ecommerce_api.domains.users.service import UserService
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.repositories.fake_shopping_cart_repo import FakeShoppingCartRepo
from tests.fakes.repositories.fake_user_repo import FakeUserRepo


@pytest.mark.asyncio
async def test_registering_user_creates_cart_end_to_end():
    bus = EventBus()
    event_register = EventRegistry(bus)
    cart_repo = FakeShoppingCartRepo()
    cart_handlers = CartEventHandlers(ShoppingCartService(cart_repo))

    event_register.register_cart_handler(cart_handlers)

    user_service = UserService(FakeUserRepo(), FakePasswordHasher(), event_bus=bus)

    user = await user_service.register(
        UserCreate(email='a@b.com', name='a', password='pw')
    )

    assert len(cart_repo.storage) == 1
    assert cart_repo.storage[1].user.id == user.id

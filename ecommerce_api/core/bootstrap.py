from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.users.events import UserRegistered


def register_event_handlers(
    event_bus: EventBus, cart_handlers: CartEventHandlers
) -> None:
    event_bus.subscribe(UserRegistered, cart_handlers.on_user_registration)

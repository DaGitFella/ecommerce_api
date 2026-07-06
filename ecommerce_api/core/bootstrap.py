from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.users.events import UserRegistered


class EventRegistry:
    def __init__ (self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def register_all(
        self, 
        cart_handler: CartEventHandlers
    ):
        self.event_bus.subscribe(UserRegistered, cart_handler.on_user_registration)
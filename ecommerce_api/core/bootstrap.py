from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.categories.handlers import CategoryEventHandlers
from ecommerce_api.domains.products.events import ProductCreated
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.users.events import UserRegistered


class EventRegistry:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def register_all(
        self, cart_handlers: CartEventHandlers, category_handlers: CategoryEventHandlers
    ):
        self.register_cart_handler(cart_handlers)
        self.register_category_handler(category_handlers)

    def register_cart_handler(self, cart_handler: CartEventHandlers):
        self.event_bus.subscribe(UserRegistered, cart_handler.on_user_registration)

    def register_category_handler(self, category_handler: CategoryEventHandlers):
        self.event_bus.subscribe(ProductCreated, category_handler.on_product_created)

from ecommerce_api.domains.users.events import UserRegistered

from .service import ShoppingCartService


class CartEventHandlers:
    def __init__(self, cart_service: ShoppingCartService) -> None:
        self.cart_service = cart_service

    async def on_user_registration(self, event: UserRegistered) -> None:
        await self.cart_service.create_default_shopping_cart(user_id=event.user_id)

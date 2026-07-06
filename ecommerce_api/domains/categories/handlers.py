from ecommerce_api.domains.products.events import ProductCreated

from .service import CategoryService


class CategoryEventHandlers:
    def __init__(self, cart_service: CategoryService) -> None:
        self.category_service = cart_service

    async def on_product_created(self, event: ProductCreated) -> None:
        [
            await self.category_service.get_or_create_category(cat)
            for cat in event.categories or []
        ]

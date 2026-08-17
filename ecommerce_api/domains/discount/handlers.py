from ecommerce_api.domains.products.events import ProductCreated

from .service import DiscountService


class DiscountEventHandlers:
    def __init__(self, discount_service: DiscountService) -> None:
        self.discount_service = discount_service

    async def on_product_created(self, event: ProductCreated) -> None:
        discounts = [
            await self.discount_service.get_or_create_discount(discount)
            for discount in event.discounts or []
        ]

        if discounts:
            event.product.discounts.extend(discounts)

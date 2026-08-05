from ecommerce_api.domains.products.events import ProductCreated

from .service import SpecificationsService


class SpecificationsEventHandlers:
    def __init__(self, specification_service: SpecificationsService) -> None:
        self.specification_service = specification_service

    async def on_product_created(self, event: ProductCreated) -> None:
        [
            await self.specification_service.get_or_create_specification(spec)
            for spec in event.specifications or []
        ]

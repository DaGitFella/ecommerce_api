from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.core.exceptions import ConflictError

from .models import Discount
from .repository import DiscountRepository
from .schema import DiscountList, DiscountSchema


class DiscountService:
    def __init__(self, repo: DiscountRepository, event_bus: EventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    async def register_discount(self, data: DiscountSchema):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Discount with name {data.name} already registered.')

        discount = self.repo.create_product(data)

        return discount

    def update_discount(self, data: DiscountSchema, id: int):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Discount with name {data.name} already registered.')
        return self.repo.update(**data.model_dump(), id=id)

    def delete_discount(self, id: int) -> None:
        product = self.repo.get_or_raise(id)

        return self.repo.delete(product.id)

    def get_discount_by_id(self, id: int) -> Discount:
        discount = self.repo.get_or_raise(id)

        return discount

    def get_discount_by_slug(self, slug: str) -> Discount:
        discount = self.repo.get_by_slug(slug)

        return discount

    def list_discounts(
        self, limit: int = 20, offset: int = 0, *filters: any
    ) -> DiscountList:
        discounts = self.repo.list(limit=limit, offset=offset, *filters)

        return {'discounts': discounts}

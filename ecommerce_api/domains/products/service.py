from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.core.exceptions import ConflictError

from .events import ProductCreated
from .repository import ProductRepository
from .schema import (
    ProductCreate,
    ProductList,
    ProductUpdate,
)


class ProductService:
    def __init__(self, repo: ProductRepository, event_bus: EventBus) -> None:
        self.repo = repo
        self.event_bus = event_bus

    async def register_product(self, data: ProductCreate):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')

        product = self.repo.create_product(data)

        await self.event_bus.publish(
            ProductCreated(categories=data.categories, product=product)
        )

        return product

    def update_product(self, data: ProductUpdate, id: int):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')
        return self.repo.update(**data.model_dump(), id=id)

    def delete_product(self, id: int) -> None:
        product = self.repo.get_or_raise(id)

        return self.repo.delete(product.id)

    def list_products(
        self, limit: int = 20, offset: int = 0, *filters: any
    ) -> ProductList:
        products = self.repo.list(limit=limit, offset=offset, *filters)

        return {'products': products}

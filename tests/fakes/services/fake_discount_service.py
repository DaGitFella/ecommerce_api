from ecommerce_api.domains.discount.service import DiscountService
from ecommerce_api.domains.products.models import Product


class FakeDiscountService(DiscountService):
    def __init__(self) -> None:
        self.calls: list[Product] = []

    async def get_or_create_discount(self, product: Product) -> None:
        self.calls.append(product)

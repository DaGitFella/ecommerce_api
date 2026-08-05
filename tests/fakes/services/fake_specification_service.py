from ecommerce_api.domains.products.models import Product
from ecommerce_api.domains.specifications.service import SpecificationsService


class FakeSpecificationsService(SpecificationsService):
    def __init__(self) -> None:
        self.calls: list[Product] = []

    async def get_or_create_specification(self, product: Product) -> None:
        self.calls.append(product)

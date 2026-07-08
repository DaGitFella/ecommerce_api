from ecommerce_api.domains.categories.service import CategoryService
from ecommerce_api.domains.products.models import Product


class FakeCategoryService(CategoryService):
    def __init__(self) -> None:
        self.calls: list[Product] = []

    async def get_or_create_category(self, product: Product) -> None:
        self.calls.append(product)

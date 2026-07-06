from ecommerce_api.domains.products.models import Product


class FakeCategoryService:
    def __init__(self) -> None:
        self.calls: list[Product] = []

    async def create_default_shopping_cart(self, product: Product) -> None:
        self.calls.append(product)

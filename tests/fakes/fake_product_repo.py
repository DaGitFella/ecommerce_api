from ecommerce_api.models import Product
from ecommerce_api.repositories.product_repo import ProductRepository
from tests.fakes.fake_base_repo import FakeBaseRepository


class FakeProductRepo(FakeBaseRepository[Product], ProductRepository):
    def __init__(self):
        super().__init__()
        self.model = Product

    def name_exists(self, name: str) -> bool:
        return any(product.name == name for product in self.storage.values())

    def get_by_name(self, name: str) -> Product | None:
        for id, instance in self.storage.items():
            if instance.name == name:
                product = instance
                return product

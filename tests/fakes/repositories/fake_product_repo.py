from ecommerce_api.domains.products.models import Product
from ecommerce_api.domains.products.repository import ProductRepository
from tests.fakes.repositories.fake_slug_and_name_repo import FakeSlugAndNameRepo


class FakeProductRepo(FakeSlugAndNameRepo[Product], ProductRepository):
    def __init__(self):
        super().__init__()
        self.model = Product

from ecommerce_api.domains.specifications.models import Specification
from ecommerce_api.domains.specifications.repository import SpecificationsRepository
from tests.fakes.repositories.fake_base_repo import FakeBaseRepository


class FakeSpecificationsRepo(
    FakeBaseRepository[Specification], SpecificationsRepository
):
    def __init__(self):
        super().__init__()
        self.model = Specification
        self.product_id = 1

    def get_by_product_id(self, product_id: int) -> Specification:
        return self.get_or_raise(product_id)

    def name_exists(self, name: str) -> bool:
        return any(spec.name == name for spec in self.storage.values())

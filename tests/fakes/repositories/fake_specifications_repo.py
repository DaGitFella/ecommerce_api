from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.specifications.repository import SpecificationKeyRepository
from tests.fakes.repositories.fake_slug_and_name_repo import FakeSlugAndNameRepo


class FakeSpecificationsRepo(
    FakeSlugAndNameRepo[SpecificationKey], SpecificationKeyRepository
):
    def __init__(self):
        super().__init__()
        self.model = SpecificationKey
        self.product_id = 1

    def get_by_product_id(self, product_id: int) -> SpecificationKey:
        return self.get_or_raise(product_id)

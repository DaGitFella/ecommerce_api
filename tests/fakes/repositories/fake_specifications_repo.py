from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.specifications.repository import SpecificationKeyRepository
from tests.fakes.repositories.fake_base_repo import FakeBaseRepository


class FakeSpecificationsRepo(
    FakeBaseRepository[SpecificationKey], SpecificationKeyRepository
):
    def __init__(self):
        super().__init__()
        self.model = SpecificationKey
        self.product_id = 1

    def get_by_product_id(self, product_id: int) -> SpecificationKey:
        return self.get_or_raise(product_id)

    def slug_exists(self, slug: str) -> bool:
        return any(spec.slug == slug for spec in self.storage.values())

    def get_by_slug(self, slug: str) -> SpecificationKey | None:
        specification = next(
            (spec for spec in self.storage.values() if spec.slug == slug), None
        )

        return specification

from sqlalchemy import select

from ecommerce_api.infrastructure.repositories.slug_and_name import (
    BaseSlugAndNameRepository,
)

from .models import SpecificationKey
from .schema import SpecificationList


class SpecificationKeyRepository(BaseSlugAndNameRepository[SpecificationKey]):
    model = SpecificationKey

    def get_by_product_id(self, product_id: int) -> SpecificationList:
        result = self.session.execute(
            select(SpecificationKey).where(SpecificationKey.product_id == product_id)
        )

        response = result.scalars().all()

        return SpecificationList(specifications=response)

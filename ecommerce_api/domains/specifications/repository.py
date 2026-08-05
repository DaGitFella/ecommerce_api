from sqlalchemy import select

from ecommerce_api.infrastructure.repositories.base import BaseRepository

from .models import SpecificationKey
from .schema import SpecificationList


class SpecificationKeyRepository(BaseRepository[SpecificationKey]):
    model = SpecificationKey

    def get_by_product_id(self, product_id: int) -> SpecificationList:
        result = self.session.execute(
            select(SpecificationKey).where(SpecificationKey.product_id == product_id)
        )

        response = result.scalars().all()

        return SpecificationList(specifications=response)

    def name_exists(self, name: str) -> bool:
        return self.session.query(self.model).filter_by(name=name).first()

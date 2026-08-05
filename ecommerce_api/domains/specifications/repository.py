from sqlalchemy import select

from ecommerce_api.core.exceptions import NotFoundError
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

    def get_or_raise(self, id: int = None, slug: str = None) -> SpecificationKey:
        if not id and not slug:
            raise ValueError("Either 'id' or 'slug' must be provided.")

        specification_by_id = self.get_by_id(id)
        specification_by_slug = self.get_by_slug(slug)

        specification = specification_by_id or specification_by_slug

        if not specification:
            raise NotFoundError('Specification not found.')

        return specification

    def get_by_slug(self, slug: str) -> SpecificationKey:
        return self.session.query(self.model).filter_by(slug=slug).first()

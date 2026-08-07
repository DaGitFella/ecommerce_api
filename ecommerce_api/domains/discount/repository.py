from sqlalchemy import func, select

from ecommerce_api.core.exceptions import NotFoundError
from ecommerce_api.infrastructure.repositories.base import BaseRepository

from .models import Discount
from .schema import DiscountSchema


class DiscountRepository(BaseRepository[Discount]):
    model = Discount

    def get_by_name(self, name: str) -> Discount:
        result = self.session.execute(select(Discount).where(Discount.name == name))
        return result.scalar_one_or_none()

    def get_by_slug(self, slug: str) -> Discount:
        result = self.session.execute(select(Discount).where(Discount.slug == slug))
        result = result.scalar_one_or_none()

        if not result:
            raise NotFoundError(f'Discount with slug {slug} not found.')

        return result

    def name_exists(self, name: str) -> bool:
        result = self.session.execute(select(func.count()).where(Discount.name == name))
        return result.scalar_one() > 0

    def create_discount(self, data: DiscountSchema) -> Discount:
        creation_data = data.model_dump(exclude={'categories'})

        return self.create(**creation_data)

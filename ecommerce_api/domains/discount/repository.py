from ecommerce_api.infrastructure.repositories.slug_and_name import (
    BaseSlugAndNameRepository,
)

from .models import Discount
from .schema import DiscountSchema


class DiscountRepository(BaseSlugAndNameRepository[Discount]):
    model = Discount

    def create_discount(self, data: DiscountSchema) -> Discount:
        creation_data = data.model_dump(exclude={'categories'})

        return self.create(**creation_data)

from ecommerce_api.infrastructure.repositories.slug_and_name import (
    BaseSlugAndNameRepository,
)

from .models import Product
from .schema import ProductCreate


class ProductRepository(BaseSlugAndNameRepository[Product]):
    model = Product

    def create_product(self, data: ProductCreate) -> Product:
        creation_data = data.model_dump(exclude={'categories'})

        return self.create(**creation_data)

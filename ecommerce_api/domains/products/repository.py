from sqlalchemy import func, select

from ecommerce_api.infrastructure.repositories.base import BaseRepository

from .models import Product
from .schema import ProductCreate


class ProductRepository(BaseRepository[Product]):
    model = Product

    def get_by_name(self, name: str):
        result = self.session.execute(select(Product).where(Product.name == name))
        return result.scalar_one_or_none()

    def name_exists(self, name: str):
        result = self.session.execute(select(func.count()).where(Product.name == name))
        return result.scalar_one() > 0

    def create_product(self, data: ProductCreate) -> Product:
        creation_data = data.model_dump(exclude={'categories'})

        return self.create(**creation_data)

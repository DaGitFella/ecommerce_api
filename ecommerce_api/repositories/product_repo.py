from sqlalchemy import func, select

from ecommerce_api.models.products import Product
from ecommerce_api.repositories.base_repo import BaseRepository
from ecommerce_api.schemas.product_schema import CreateProduct


class ProductRepository(BaseRepository[Product]):
    model = Product

    def get_by_name(self, name: str):
        result = self.session.execute(select(Product).where(Product.name == name))
        return result.scalar_one_or_none()

    def name_exists(self, name: str):
        result = self.session.execute(select(func.count()).where(Product.name == name))
        return result.scalar_one() > 0

    def create_product(self, data: CreateProduct):
        return self.create(**data.model_dump())

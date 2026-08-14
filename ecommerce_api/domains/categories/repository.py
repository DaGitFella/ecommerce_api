from ecommerce_api.infrastructure.repositories.slug_and_name import BaseSlugAndNameRepository

from .models import Category
from .schema import CategoryCreate


class CategoryRepository(BaseSlugAndNameRepository[Category]):
    model = Category

    def create_category(self, data: CategoryCreate) -> Category:
        creation_data = data.model_dump()

        return self.create(**creation_data)

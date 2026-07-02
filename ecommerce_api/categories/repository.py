from sqlalchemy import func, select

from ecommerce_api.categories.models import Category
from ecommerce_api.core.exceptions import NotFoundError
from ecommerce_api.infrastructure.repositories.base import BaseRepository

from .schema import CategoryCreate


class CategoryRepository(BaseRepository[Category]):
    model = Category

    def get_by_slug(self, slug: str) -> Category:
        return self.session.query(self.model).filter_by(slug=slug).first()

    def slug_exists(self, slug: str) -> bool:
        result = self.session.execute(select(func.count()).where(Category.slug == slug))
        return result.scalar_one() > 0

    def get_or_raise(self, id: int = None, slug: str = None) -> Category:
        if not id and not slug:
            raise ValueError("Either 'id' or 'slug' must be provided.")

        category_by_id = self.get_by_id(id)
        category_by_slug = self.get_by_slug(slug)

        category = category_by_id or category_by_slug

        if not category:
            raise NotFoundError('Category not found.')
        return category

    def create_category(self, data: CategoryCreate) -> Category:
        creation_data = data.model_dump()

        return self.create(**creation_data)

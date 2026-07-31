from ecommerce_api.core.exceptions import ConflictError

from .models import Category
from .repository import CategoryRepository
from .schema import CategoryCreate, CategoryList, CategoryUpdate


class CategoryService:
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.repo = category_repo

    def create_category(self, category_data: CategoryCreate) -> Category:
        if self.repo.slug_exists(category_data.slug):
            raise ConflictError(
                f'Category with slug {category_data.slug} already exists.'
            )

        category_instance = self.repo.create_category(category_data)

        return category_instance

    def update_category(
        self, category_id: int, category_data: CategoryUpdate
    ) -> Category:

        if self.repo.slug_exists(category_data.slug):
            raise ConflictError(
                f'A category with the slug {category_data.slug} already exists.'
            )

        update_data = category_data.model_dump()

        return self.repo.update(category_id, **update_data)

    async def get_or_create_category(self, category_data: CategoryCreate) -> Category:
        existing_category = self.repo.get_by_slug(category_data.slug)

        if existing_category:
            return existing_category

        new_category = self.repo.create(**category_data.model_dump())
        return new_category

    def delete_category(self, id: int) -> None:
        category = self.repo.get_or_raise(id)

        self.repo.delete(category.id)

    def get_category(self, slug: str = None, id: int = None):
        return self.repo.get_or_raise(slug=slug, id=id)

    def list_categories(
        self, limit: int = 20, offset: int = 0, *filters
    ) -> CategoryList:
        categories = self.repo.list(limit=limit, offset=offset, *filters)

        return {'categories': categories}

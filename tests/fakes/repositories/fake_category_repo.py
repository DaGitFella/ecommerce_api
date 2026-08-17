from ecommerce_api.core.exceptions import NotFoundError
from ecommerce_api.domains.categories.models import Category
from ecommerce_api.domains.categories.repository import CategoryRepository
from tests.fakes.repositories.fake_slug_and_name_repo import FakeSlugAndNameRepo


class FakeCategoryRepo(FakeSlugAndNameRepo[Category], CategoryRepository):
    def __init__(self):
        super().__init__()
        self.model = Category

    def get_or_raise(self, id: int = None, slug: str = None) -> Category | None:
        if not id and not slug:
            raise ValueError("Either 'id' or 'slug' must be provided.")

        category_by_id = self.get_by_id(id)
        category_by_slug = self.get_by_slug(slug)

        category = category_by_id or category_by_slug

        if not category:
            raise NotFoundError('Category not found.')
        return category

from ecommerce_api.domains.categories.models import Category
from ecommerce_api.domains.categories.repository import CategoryRepository
from tests.fakes.repositories.fake_slug_and_name_repo import FakeSlugAndNameRepo


class FakeCategoryRepo(FakeSlugAndNameRepo[Category], CategoryRepository):
    def __init__(self):
        super().__init__()
        self.model = Category

from ecommerce_api.domains.discount.models import Discount
from ecommerce_api.domains.discount.repository import DiscountRepository
from tests.fakes.repositories.fake_slug_and_name_repo import FakeSlugAndNameRepo


class FakeDiscountRepo(FakeSlugAndNameRepo[Discount], DiscountRepository):
    def __init__(self):
        super().__init__()
        self.model = Discount

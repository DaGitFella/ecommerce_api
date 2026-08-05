from ecommerce_api.domains.shopping_carts.models import ShoppingCart
from ecommerce_api.domains.shopping_carts.repository import ShoppingCartRepository
from tests.fakes.repositories.fake_base_repo import FakeBaseRepository


class FakeShoppingCartRepo(FakeBaseRepository[ShoppingCart], ShoppingCartRepository):
    def __init__(self):
        super().__init__()
        self.model = ShoppingCart
        self._user_id = 1

    def get_by_user_id(self, user_id=id) -> ShoppingCart:
        return self.get_or_raise(user_id)

from ecommerce_api.models import ShoppingCart
from ecommerce_api.repositories.shopping_cart_repo import ShoppingCartRepository
from ecommerce_api.schemas.shopping_cart_schema import ShoppingCartCreate
from tests.fakes.fake_base_repo import FakeBaseRepository


class FakeShoppingCartRepo(FakeBaseRepository[ShoppingCart], ShoppingCartRepository):
    def __init__(self):
        super().__init__()
        self.model = ShoppingCart
        self._user_id = 1

    def create_default_shopping_cart(self, data: ShoppingCartCreate) -> ShoppingCart:
        return self.create(data, self._user_id)

    def get_by_user_id(self, user_id=id) -> ShoppingCart:
        return self.get_or_raise(user_id)

from sqlalchemy import select

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.models import ShoppingCart
from ecommerce_api.repositories.base_repo import BaseRepository
from ecommerce_api.schemas.shopping_cart_schema import ShoppingCartCreate


class ShoppingCartRepository(BaseRepository[ShoppingCart]):
    model = ShoppingCart

    def get_by_user_id(self, user_id: int) -> ShoppingCart | None:
        result = self.session.execute(
            select(ShoppingCart).where(ShoppingCart.user_id == user_id)
        )
        return result.scalar_one_or_none()

    def create_default_shopping_cart(self, data: ShoppingCartCreate) -> ShoppingCart:
        # User id must be gotten from current user whe it's implemented
        return self.create(shipping_type=ShippingTypes.DELIVERY, user_id=1)

from sqlalchemy import select

from ecommerce_api.models import ShoppingCart
from ecommerce_api.repositories.base_repo import BaseRepository


class ShoppingCartRepository(BaseRepository[ShoppingCart]):
    model = ShoppingCart

    def get_by_user_id(self, user_id: int) -> ShoppingCart | None:
        result = self.session.execute(
            select(ShoppingCart).where(ShoppingCart.user_id == user_id)
        )
        return result.scalar_one_or_none()

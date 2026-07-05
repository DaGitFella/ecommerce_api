import typing

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.core.exceptions import MethodNotAllowedError
from ecommerce_api.domains.users.models import User

from .models import ShoppingCart
from .repository import ShoppingCartRepository
from .schema import (
    ShoppingCartList,
    ShoppingCartUpdate,
)


class ShoppingCartService:
    def __init__(self, repo: ShoppingCartRepository) -> None:
        self.repo = repo

    async def create_default_shopping_cart(self, user: User) -> ShoppingCart:
        return self.repo.create(
            shipping_type=ShippingTypes.DELIVERY, user_id=user.id, user=user
        )

    def update_shopping_cart(self, id: int, data: ShoppingCartUpdate) -> ShoppingCart:
        return self.repo.update(id=id, **data.model_dump())

    @typing.override
    def delete(self, id: int) -> None:
        raise MethodNotAllowedError(
            message='Deleting shopping cart is not allowed',
            detail='Deleting shopping cart is not allowed',
            allow=['GET', 'POST', 'PUT'],
        )

    def list_shopping_carts(self, limit: int = 20, offset: int = 0) -> ShoppingCartList:
        shopping_carts = self.repo.list(limit=limit, offset=offset)

        returning_items = ShoppingCartList.model_validate({
            'shopping_carts': shopping_carts
        })

        return returning_items

    def get_shopping_cart_or_404(self, id: int) -> ShoppingCart:
        return self.repo.get_or_raise(id)

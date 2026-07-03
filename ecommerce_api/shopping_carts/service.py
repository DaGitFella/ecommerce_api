import typing

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.core.exceptions import MethodNotAllowedError
from ecommerce_api.shopping_carts.repository import ShoppingCartRepository
from ecommerce_api.shopping_carts.schema import ShoppingCartList, ShoppingCartUpdate
from ecommerce_api.users.models import User

from .models import ShoppingCart


class ShoppingCartService:
    def __init__(self, repo: ShoppingCartRepository) -> None:
        self.repo = repo

    def create_default_shopping_cart(self, user: User) -> ShoppingCart:
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

    def list_shopping_carts(
        self, limit: int = 20, offset: int = 0, *filters: any
    ) -> ShoppingCartList:
        shopping_carts = self.repo.list(limit=limit, offset=offset, *filters)

        return {'shopping_carts': shopping_carts}

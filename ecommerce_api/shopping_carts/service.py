import typing

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.core.exceptions import MethodNotAllowedError
from ecommerce_api.shopping_carts.repository import ShoppingCartRepository
from ecommerce_api.shopping_carts.schema import (
    ShoppingCartUpdate,
)
from ecommerce_api.users.models import User

from .models import ShoppingCart

# this is provisory until current user is implemented,
# then the user_id will be gotten from the current user


class ShoppingCartService:
    def __init__(self, repo: ShoppingCartRepository) -> None:
        self.repo = repo

    def create_default_shopping_cart(self, user: User) -> ShoppingCart:
        # User must be gotten from current user whe it's implemented
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

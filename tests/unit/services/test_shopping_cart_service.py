import pytest

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.core.exceptions import MethodNotAllowedError, NotFoundError
from ecommerce_api.shopping_carts.schema import (
    ShoppingCartUpdate,
)


def test_get_shopping_cart_must_return_shopping_cart_instance(
    fake_user_service_with_users,
):
    user_service = fake_user_service_with_users
    cart_service = user_service.shopping_cart_service

    cart = cart_service.repo.get_by_id(id=1)

    assert cart.id == 1
    assert cart.user_id == 1
    assert cart.shipping_type == ShippingTypes.DELIVERY
    assert cart.shipping_cost == 0


def test_get_shopping_cart_by_user_id_must_return_shopping_cart_instance(
    fake_user_service_with_users,
):
    user_service = fake_user_service_with_users
    cart_service = user_service.shopping_cart_service

    cart = cart_service.repo.get_by_user_id(user_id=1)

    assert cart.id == 1
    assert cart.user_id == 1
    assert cart.shipping_type == ShippingTypes.DELIVERY
    assert cart.shipping_cost == 0


def test_get_shopping_cart_must_return_not_found(
    fake_user_service_with_users,
):
    service = fake_user_service_with_users.shopping_cart_service

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(id=3)


def test_get_shopping_cart_list_must_return_list_instance(
    fake_user_service_with_users,
):
    service = fake_user_service_with_users.shopping_cart_service

    cart_list = service.repo.list()

    assert isinstance(cart_list, list)


def test_delete_shopping_cart_must_return_MethodNotAllowedError(
    fake_user_service_with_users,
):
    service = fake_user_service_with_users.shopping_cart_service

    with pytest.raises(MethodNotAllowedError):
        service.delete(id=1)


def test_update_shopping_cart_must_return_shopping_cart_instance(
    fake_user_service_with_users,
):
    service = fake_user_service_with_users.shopping_cart_service

    data = ShoppingCartUpdate(shipping_type=ShippingTypes.PICKUP)

    shopping_cart = service.update_shopping_cart(id=1, data=data)

    assert shopping_cart.id == 1
    assert shopping_cart.shipping_type == data.shipping_type

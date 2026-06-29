from ecommerce_api.core.constants import ShippingTypes

from ecommerce_api.models.shopping_cart import ShippingTypes

from ecommerce_api.schemas.shopping_cart_schema import (
    ShoppingCartCreate, ShoppingCartList, ShoppingCartUpdate,
    ShoppingCartPublic
)

def test_get_shopping_cart_must_return_shopping_cart_instance(
    fake_shopping_cart_service_with_items,
):
    service = fake_shopping_cart_service_with_items

    cart = service.repo.get_or_raise(id=1)

    assert cart.id == 1
    assert cart.user_id == 1
    assert cart.shipping_type == ShippingTypes.DELIVERY
    assert cart.shipping_cost is None


def test_get_shopping_cart_by_user_id_must_return_shopping_cart_instance(
    fake_shopping_cart_service_with_items,
):
    service = fake_shopping_cart_service_with_items

    cart = service.get_by_user_id(id=1)

    assert cart.id == 1
    assert cart.user_id == 1
    assert cart.shipping_type == ShippingTypes.DELIVERY
    assert cart.shipping_cost is None


def test_get_shopping_cart_must_return_not_found(
    fake_shopping_cart_service_with_items,
):
    service = fake_shopping_cart_service_with_items

    cart = service.repo.get_or_raise(id=1)

    assert cart.id == 1
    assert cart.user_id == 1
    assert cart.shipping_type == ShippingTypes.DELIVERY
    assert cart.shipping_cost is None

def test_get_shopping_cart_list_must_return_list_instance(
    fake_shopping_cart_service_with_items
):
    service = fake_shopping_cart_service_with_items
    
    cart_list = service.repo.list()
    
    assert isinstance(cart_list, list)

def test_delete_shopping_cart_must_return_None(
    fake_shopping_cart_service_with_items
):
    service = fake_shopping_cart_service_with_items
    
    result = service.repo.delete(id=1)
    
    assert result == None

def test_update_shopping_cart_must_return_shopping_cart_instance(
    fake_shopping_cart_service_with_items
):
    service = fake_shopping_cart_service_with_items
    
    data = ShoppingCartCreate(
        shipping_type=ShippingTypes.DELIVERY,
    )
    
    shopping_cart = service.create_shopping_cart(data)
    
    assert shopping_cart.id == 1
    assert shopping_cart.name == data.shipping_type

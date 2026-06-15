from ecommerce_api.core.constants import ShippingTypes


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

from datetime import datetime, timedelta

import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.domains.discount.schema import DiscountSchema


@pytest.mark.asyncio
async def test_create_discount_must_return_discount(fake_discount_service_with_discounts):
    service = fake_discount_service_with_discounts

    data = DiscountSchema(
        name='dia da casa nova',
        slug='house',
        value=.5,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=9),
    )

    discount = await service.register_discount(data)

    assert discount.id == 3
    assert discount.name == data.name
    assert discount.value == data.value

@pytest.mark.asyncio
async def test_create_discount_must_return_conflict_error(
    fake_discount_service_with_discounts,
):
    service = fake_discount_service_with_discounts

    data = DiscountSchema(
        name='dia do eletronico',
        slug='electronics',
        value=.5,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=9),
    )

    with pytest.raises(ConflictError):
        await service.register_discount(data)


def test_delete_discount_must_return_none(fake_discount_service_with_discounts):
    service = fake_discount_service_with_discounts

    result = service.delete_discount(id=1)

    assert result is None

    with pytest.raises(NotFoundError):
        service.get_discount_by_id(id=1)


def test_delete_discount_must_return_not_found(fake_discount_service_with_discounts):
    service = fake_discount_service_with_discounts

    unreachable_id = 999
    
    with pytest.raises(NotFoundError):
        service.delete_discount(unreachable_id)


def test_update_product_must_return_product_instance(
    fake_product_service_with_products,
):
    service = fake_product_service_with_products

    update_data = ProductUpdate(
        name='Maquina sinistra',
        description='Máquina de baixa tração',
        price=5,
        stock=999,
    )

    updated_product = service.update_product(data=update_data, id=1)

    assert updated_product.id == 1
    assert updated_product.name == update_data.name
    assert updated_product.description == update_data.description
    assert updated_product.price == update_data.price
    assert updated_product.stock == update_data.stock


def test_update_product_must_return_conflict_error(fake_product_service_with_products):
    service = fake_product_service_with_products

    update_data = ProductUpdate(
        name='Máquina épica',
        description='Máquina de baixa tração',
        price=5,
        stock=999,
    )

    with pytest.raises(ConflictError):
        service.update_product(data=update_data, id=1)


def test_get_product_must_return_product_instance(fake_product_service_with_products):
    service = fake_product_service_with_products

    product = service.repo.get_or_raise(id=1)

    attrs = ['name', 'description', 'id', 'price', 'stock']

    for attr in attrs:
        assert hasattr(product, attr)


def test_get_product_must_return_not_found(fake_product_service):
    service = fake_product_service

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(id=1)


def test_get_product_list_must_return_list_instance(fake_product_service_with_products):
    service = fake_product_service_with_products

    product_list = service.repo.list()

    assert isinstance(product_list, list)

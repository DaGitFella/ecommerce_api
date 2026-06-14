import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.schemas.product_schema import CreateProduct, UpdateProduct


def test_create_product_must_return_product(fake_product_service):
    service = fake_product_service

    data = CreateProduct(
        name='maquina legal',
        description='maquina de alta tração incrivel',
        price=999,
        stock=5,
    )

    product = service.register_product(data)

    assert product.id == 1
    assert product.name == data.name
    assert product.description == data.description
    assert product.price == data.price
    assert product.stock == data.stock


def test_create_product_must_return_conflict_error(
    fake_product_service_with_products,
):
    service = fake_product_service_with_products

    data = CreateProduct(
        name='maquina legal', description='maquina de alta tração', price=999, stock=5
    )

    with pytest.raises(ConflictError):
        service.register_product(data)


def test_delete_product_must_return_none(fake_product_service_with_products):
    service = fake_product_service_with_products

    result = service.delete_product(id=1)

    assert result is None


def test_delete_product_must_return_not_found(fake_product_service):
    service = fake_product_service

    with pytest.raises(NotFoundError):
        service.delete_product(id=1)


def test_update_product_must_return_product_instance(
    fake_product_service_with_products,
):
    service = fake_product_service_with_products

    update_data = UpdateProduct(
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

    update_data = UpdateProduct(
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

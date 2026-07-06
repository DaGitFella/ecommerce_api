import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.domains.categories.schema import CategoryCreate
from ecommerce_api.domains.products.events import ProductCreated
from ecommerce_api.domains.products.schema import ProductCreate, ProductUpdate
from ecommerce_api.domains.products.service import ProductService
from tests.fakes.events.fake_event_bus import FakeEventBus
from tests.fakes.repositories.fake_product_repo import FakeProductRepo


@pytest.mark.asyncio
async def test_create_product_must_return_product(fake_product_service):
    service = fake_product_service

    data = ProductCreate(
        name='maquina legal',
        description='maquina de alta tração incrivel',
        price=999,
        stock=5,
    )

    product = await service.register_product(data)

    assert product.id == 1
    assert product.name == data.name
    assert product.description == data.description
    assert product.price == data.price
    assert product.stock == data.stock


@pytest.mark.asyncio
async def test_create_product_publishes_product_created_event():
    bus = FakeEventBus()
    service = ProductService(user_repo=FakeProductRepo(), event_bus=bus)

    test_category = CategoryCreate(name='Eletronicos', slug='eletronics')

    test_product = ProductCreate(
        name='test', price=2.99, strock=6, categories=[test_category]
    )

    await service.register_product(test_product)

    assert len(bus.published) > 0
    assert isinstance(bus.published[0], ProductCreated)
    assert bus.published[0].user.id == 1


@pytest.mark.asyncio
async def test_create_product_must_return_conflict_error(
    fake_product_service_with_products,
):
    service = fake_product_service_with_products

    data = ProductCreate(
        name='maquina legal', description='maquina de alta tração', price=999, stock=5
    )

    with pytest.raises(ConflictError):
        await service.register_product(data)


def test_delete_product_must_return_none(fake_product_service_with_products):
    service = fake_product_service_with_products

    result = service.delete_product(id=1)

    assert result is None

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(id=1)


def test_delete_product_must_return_not_found(fake_product_service):
    service = fake_product_service

    with pytest.raises(NotFoundError):
        service.delete_product(id=1)


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

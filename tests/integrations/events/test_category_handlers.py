import pytest

from ecommerce_api.core.bootstrap import EventRegistry
from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.domains.categories.handlers import CategoryEventHandlers
from ecommerce_api.domains.categories.schema import CategoryCreate
from ecommerce_api.domains.categories.service import CategoryService
from ecommerce_api.domains.products.schema import ProductCreate
from ecommerce_api.domains.products.service import ProductService
from tests.fakes.repositories.fake_category_repo import FakeCategoryRepo
from tests.fakes.repositories.fake_product_repo import FakeProductRepo


@pytest.mark.asyncio
async def test_registering_product_creates_new_category_end_to_end():
    bus = EventBus()
    event_register = EventRegistry(bus)
    category_repo = FakeCategoryRepo()
    category_handler = CategoryEventHandlers(CategoryService(category_repo))

    event_register.register_category_handler(category_handler)

    product_service = ProductService(event_bus=bus, repo=FakeProductRepo())

    categories = [CategoryCreate(name='New Category', slug='new-category')]

    product = await product_service.register_product(
        ProductCreate(
            categories=categories,
            description='produto de teste',
            name='teste',
            price=1,
            stock=2,
        )
    )

    assert len(category_repo.storage) == 1
    assert category_repo.storage[1].products[0].id == product.id

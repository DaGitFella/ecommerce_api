import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.domains.categories.models import Category
from ecommerce_api.domains.categories.schema import CategoryCreate, CategoryUpdate


@pytest.mark.asyncio
async def test_create_category_must_return_category_instance(fake_category_service):
    service = fake_category_service

    new_category_data = CategoryCreate(name='Electronics', slug='electronics')

    result = await service.get_or_create_category(new_category_data)

    assert isinstance(result, Category)
    assert result.name == 'Electronics'
    assert result.slug == 'electronics'


def test_get_category_by_id_must_return_category_instance(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_id = 1

    category_instance = service.get_category(id=category_id)

    assert isinstance(category_instance, Category)
    assert category_instance.id == category_id
    assert category_instance.name == 'Electronics'
    assert category_instance.slug == 'electronics'


def test_get_category_by_id_must_return_not_found_error_if_category_does_not_exist(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_id = 999  # An ID that doesn't exist

    with pytest.raises(NotFoundError):
        service.get_category(category_id)


def test_get_category_by_slug_must_return_category_instance(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_slug = 'electronics'

    category_instance = service.get_category(category_slug)

    assert isinstance(category_instance, Category)
    assert category_instance.slug == category_slug
    assert category_instance.name == 'Electronics'


def test_get_category_by_slug_must_return_not_found_error_if_category_does_not_exist(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_slug = 'non-existent'

    with pytest.raises(NotFoundError):
        service.get_category(category_slug)


def test_delete_category_must_return_none_and_remove_category_from_products(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_id = 1

    result = service.delete_category(category_id)

    assert result is None

    with pytest.raises(NotFoundError):
        service.get_category(category_id)


def test_update_category_must_return_category_instance_and_updated_product_categories(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_id = 1

    updated_category_data = CategoryUpdate(
        name='Updated Electronics', slug='updated-electronics'
    )

    updated_category_instance = service.update_category(
        category_id=category_id, category_data=updated_category_data
    )

    assert isinstance(updated_category_instance, Category)
    assert updated_category_instance.name == updated_category_data.name
    assert updated_category_instance.slug == updated_category_data.slug


def test_update_category_must_return_conflict_error(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    category_id = 1

    updated_category_data = CategoryUpdate(name='Books', slug='books')

    with pytest.raises(ConflictError):
        service.update_category(
            category_id=category_id, category_data=updated_category_data
        )

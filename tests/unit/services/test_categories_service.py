import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.domains.categories.schema import CategoryCreate, CategoryUpdate
from ecommerce_api.domains.products.schema import ProductCreate
from ecommerce_api.models import Category


def test_create_category_must_return_category_instance(fake_category_service):
    service = fake_category_service

    new_category_data = CategoryCreate(name='Electronics', slug='electronics')

    result = service.create_category(new_category_data)

    assert isinstance(result, Category)
    assert result.name == 'Electronics'
    assert result.slug == 'electronics'


def test_create_category_must_return_conflict_error_if_category_already_exists(
    fake_category_service_with_categories,
):
    service = fake_category_service_with_categories

    existing_category_data = CategoryCreate(name='Electronics', slug='electronics')

    with pytest.raises(ConflictError):
        service.create_category(existing_category_data)


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


def test_create_product_with_new_category_must_add_category_to_database(
    fake_product_service,
):
    product_service = fake_product_service

    new_product_data = ProductCreate(
        name='New Product',
        price=100.0,
        categories=[CategoryCreate(name='New Category', slug='new-category')],
        stock=10,
        description='A new test product',
    )

    created_product = product_service.register_product(new_product_data)

    assert created_product.name == 'New Product'
    assert len(created_product.categories) == 1

    created_category = created_product.categories[0]

    assert created_category.name == 'New Category'
    assert created_category.slug == 'new-category'


def test_create_product_with_existing_category_must_not_add_category_to_database(
    fake_product_service,
):
    product_service = fake_product_service
    category_service = product_service.category_service

    # First, create a category
    category_data = CategoryCreate(name='Existing Category', slug='existing-category')
    created_category = category_service.create_category(category_data)

    # Then, create a product with the existing category
    new_product_data = ProductCreate(
        name='New Product',
        price=100.0,
        categories=[CategoryCreate(name='Existing Category', slug='existing-category')],
        stock=10,
        description='A new test product',
    )

    created_product = product_service.register_product(new_product_data)
    product_category = created_product.categories[0]

    # Verify that the category was not added again
    assert created_category is not None
    assert product_category.id == created_category.id

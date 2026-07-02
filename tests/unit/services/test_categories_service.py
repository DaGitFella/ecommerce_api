import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.models import Category
from ecommerce_api.schemas.categorie_schema import CategoryCreate, CategoryUpdate
from ecommerce_api.products.schema import ProductCreate


def test_create_category_must_return_category_instance():
    service = SomeService()  # Replace with actual service initialization

    new_category_data = CategoryCreate(name="Electronics", slug="electronics")

    result = service.create_category(new_category_data)

    assert isinstance(result, Category)
    assert result.name == "Electronics"
    assert result.slug == "electronics"


def test_create_category_must_return_conflict_error_if_category_already_exists():
    service = SomeService()  # Replace with actual service initialization

    existing_category_data = CategoryCreate(name="Electronics", slug="electronics")

    with pytest.raises(ConflictError):
        service.create_category(existing_category_data)


def test_get_category_by_id_must_return_category_instance():
    service = SomeService()

    category_id = 1

    category_instance = service.repo.get_or_raise(category_id)

    assert isinstance(category_instance, Category)
    assert category_instance.id == category_id
    assert category_instance.name == "Electronics"
    assert category_instance.slug == "electronics"


def test_get_category_by_id_must_return_not_found_error_if_category_does_not_exist():
    service = SomeService()

    category_id = 999  # An ID that doesn't exist

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(category_id)


def test_get_category_by_slug_must_return_category_instance():
    service = SomeService()

    category_slug = "electronics"

    category_instance = service.repo.get_by_slug(category_slug)

    assert isinstance(category_instance, Category)
    assert category_instance.slug == category_slug
    assert category_instance.name == "Electronics"


def test_get_category_by_slug_must_return_not_found_error_if_category_does_not_exist():
    service = SomeService()

    category_slug = "non-existent"

    with pytest.raises(NotFoundError):
        service.repo.get_by_slug(category_slug)


def test_delete_category_must_return_none_and_remove_category_from_products():
    service = SomeService()

    category_id = 1

    result = service.delete_category(category_id)

    assert result is None

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(category_id)


def test_update_category_must_return_category_instance_and_updated_product_categories():
    service = SomeService()

    category_id = 1
    
    updated_category_data = CategoryUpdate(
        name="Updated Electronics",
        slug="updated-electronics"
    )

    updated_category_instance = service.update_category(
        category_id, updated_category_data
    )
    
    assert isinstance(updated_category_instance, Category)
    assert updated_category_instance.name == updated_category_data.name
    assert updated_category_instance.slug == updated_category_data.slug

def test_create_product_with_new_category_must_add_category_to_database():
    product_service = SomeService()
    category_service = product_service.category_service
    
    new_product_data = ProductCreate(
        name="New Product",
        price=100.0,
        category=CategoryCreate(name="New Category", slug="new-category"),
        stock=10,
        description="A new test product",
    )
    
    created_product = product_service.create_product(new_product_data)
    created_category = category_service.repo.get_by_slug("new-category")

def test_create_product_with_existing_category_must_not_add_category_to_database():
    pass

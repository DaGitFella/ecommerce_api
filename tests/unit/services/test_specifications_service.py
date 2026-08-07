import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.specifications.schema import SpecificationSchema


@pytest.mark.asyncio
def test_create_specification_must_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    new_specification_data = SpecificationSchema(name='Marca', slug='brand')

    result = service.get_or_create_specification(new_specification_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Marca'
    assert result.slug == 'brand'


@pytest.mark.asyncio
def test_get_or_create_specification_should_return_existing_specification(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    existing_specification_data = SpecificationSchema(name='Color', slug='color')

    result = service.get_or_create_specification(existing_specification_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
def test_get_specification_by_slug_should_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    slug = 'color'

    result = service.get_specification_by_slug(slug)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
def test_get_specification_by_id_should_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    specification = service.get_specification_by_slug('color')

    result = service.get_specification_by_id(specification.id)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
def test_get_specification_by_id_should_return_not_found_error(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    non_existent_id = 999  # An ID that doesn't exist

    with pytest.raises(NotFoundError):
        service.get_specification_by_id(non_existent_id)


@pytest.mark.asyncio
def test_get_specification_by_slug_should_return_not_found_error(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    non_existent_slug = 'non-existent'  # A slug that doesn't exist

    with pytest.raises(NotFoundError):
        service.get_specification_by_slug(non_existent_slug)


def test_update_should_return_updated_specification(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    specification = service.get_specification_by_slug('color')

    updated_data = SpecificationSchema(name='Updated Color', slug='updated-color')

    result = service.update_specification(specification.id, updated_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Updated Color'
    assert result.slug == 'updated-color'


def test_update_should_raise_conflict_error_for_existing_slug(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    specification = service.get_specification_by_slug('color')

    # Attempt to update the specification with a slug that already exists
    updated_data = SpecificationSchema(name='Updated Color', slug='size')

    with pytest.raises(ConflictError):
        service.update_specification(specification.id, updated_data)


def test_delete_specification_should_remove_specification(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    specification = service.get_specification_by_slug('color')

    service.delete_specification(specification.id)

    with pytest.raises(NotFoundError):
        service.get_specification_by_id(specification.id)


def test_list_specifications_should_return_specification_list(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    result = service.list_specifications()

    assert isinstance(result, dict)
    assert 'specifications' in result
    assert len(result['specifications']) > 0

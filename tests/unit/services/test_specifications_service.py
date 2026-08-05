import pytest

from ecommerce_api.core.exceptions import NotFoundError
from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.specifications.schema import SpecificationSchema


@pytest.mark.asyncio
async def test_create_specification_must_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    new_specification_data = SpecificationSchema(name='Marca', slug='brand')

    result = await service.get_or_create_specification(new_specification_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Marca'
    assert result.slug == 'brand'


@pytest.mark.asyncio
async def test_get_or_create_specification_should_return_existing_specification(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    existing_specification_data = SpecificationSchema(name='Color', slug='color')

    result = await service.get_or_create_specification(existing_specification_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
async def test_get_specification_by_slug_should_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    slug = 'color'

    result = await service.get_specification(slug)

    breakpoint()

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
async def test_get_specification_by_id_should_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    specification = await service.get_specification_by_slug('color')

    result = await service.get_specification(specification.id)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'


@pytest.mark.asyncio
async def test_get_specification_by_id_should_return_not_found_error(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    non_existent_id = 999  # An ID that doesn't exist

    with pytest.raises(NotFoundError):
        await service.get_specification(non_existent_id)


@pytest.mark.asyncio
async def test_get_specification_by_slug_should_return_not_found_error(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    non_existent_slug = 'non-existent'  # A slug that doesn't exist

    with pytest.raises(NotFoundError):
        await service.get_specification(non_existent_slug)

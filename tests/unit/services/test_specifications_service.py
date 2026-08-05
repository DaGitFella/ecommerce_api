import pytest

from ecommerce_api.domains.specifications.models import SpecificationKey
from ecommerce_api.domains.specifications.schema import SpecificationSchema


@pytest.mark.asyncio
async def test_create_specification_must_return_specification_instance(
    fake_specifications_service_with_specifications,
):
    service = fake_specifications_service_with_specifications

    new_specification_data = SpecificationSchema(name='Color', slug='color')

    result = await service.get_or_create_specification(new_specification_data)

    assert isinstance(result, SpecificationKey)
    assert result.name == 'Color'
    assert result.slug == 'color'

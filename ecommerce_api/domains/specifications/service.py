from ecommerce_api.core.exceptions import ConflictError, NotFoundError

from .models import SpecificationKey
from .repository import SpecificationKeyRepository
from .schema import SpecificationList, SpecificationSchema


class SpecificationsService:
    def __init__(self, specifications_repo: SpecificationKeyRepository) -> None:
        self.repo = specifications_repo

    def update_specification(
        self, specification_id: int, specification_data: SpecificationSchema
    ) -> SpecificationKey:

        if self.repo.slug_exists(specification_data.slug):
            raise ConflictError(
                f'A specification with the slug {specification_data.slug} \
                    already exists.'
            )

        update_data = specification_data.model_dump()

        return self.repo.update(specification_id, **update_data)

    def get_or_create_specification(
        self, specification_data: SpecificationSchema
    ) -> SpecificationKey:
        existing_specification = self.repo.get_by_slug(specification_data.slug)

        if existing_specification:
            return existing_specification

        new_specification = self.repo.create(**specification_data.model_dump())
        return new_specification

    def delete_specification(self, id: int) -> None:
        specification = self.repo.get_or_raise(id)

        self.repo.delete(specification.id)

    def get_specification_by_id(self, id: int) -> SpecificationKey:
        return self.repo.get_or_raise(id=id)

    def get_specification_by_slug(self, slug: str) -> SpecificationKey:
        result = self.repo.get_by_slug(slug=slug)

        if not result:
            raise NotFoundError(f'Specification with slug {slug} not found.')

        return result

    def list_specifications(
        self, limit: int = 20, offset: int = 0, *filters
    ) -> SpecificationList:
        specifications = self.repo.list(limit=limit, offset=offset, *filters)

        return {'specifications': specifications}

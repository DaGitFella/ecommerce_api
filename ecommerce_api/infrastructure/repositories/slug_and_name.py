from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Mapped

from ecommerce_api.core.exceptions import NotFoundError

from .base import BaseRepository, MappedModel


class HasSlugAndName(MappedModel):
    name: Mapped[str]
    slug: Mapped[str]


SlugAndNameIT = TypeVar('SlugAndNameIT', bound=HasSlugAndName)


class BaseSlugAndNameRepository(BaseRepository[SlugAndNameIT]):
    model: type[SlugAndNameIT]

    def get_by_name(self, name: str):
        result = self.session.execute(select(self.model).where(self.model.name == name))
        return result.scalar_one_or_none()

    def name_exists(self, name: str):
        result = self.session.execute(
            select(func.count()).where(self.model.name == name)
        )
        return result.scalar_one() > 0

    def get_by_slug(self, slug: str) -> SlugAndNameIT:
        result = self.session.execute(select(self.model).where(self.model.slug == slug))
        result = result.scalar_one_or_none()

        if not result:
            raise NotFoundError(f'{self.model.__name__} with slug {slug} not found.')

        return result

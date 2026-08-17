from typing import TypeVar

from sqlalchemy.orm import Mapped

from .fake_base_repo import FakeBaseRepository, MappedModel


class HasNameAndSlug(MappedModel):
    name: Mapped[str]
    slug: Mapped[str]


NameAndSlugIT = TypeVar('NameAndSlugIT', bound=HasNameAndSlug)


class FakeSlugAndNameRepo(FakeBaseRepository[NameAndSlugIT]):
    model: NameAndSlugIT

    def slug_exists(self, slug: str) -> bool:
        return any(category.slug == slug for category in self.storage.values())

    def get_by_slug(self, slug: str) -> NameAndSlugIT | None:
        instance = next(
            (instance for instance in self.storage.values() if instance.slug == slug),
            None,
        )

        return instance

    def get_by_name(self, name: str):
        instance = next(
            (instance for instance in self.storage.values() if instance.name == name),
            None,
        )

        return instance

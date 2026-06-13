from typing import Any, Generic, Protocol, TypeVar

from sqlalchemy.orm import Mapped

from ecommerce_api.core.exceptions import NotFoundError


class MappedModel(Protocol):
    __tablename__: str
    id: Mapped[int]


ModelT = TypeVar('ModelT', bound=MappedModel)


class FakeBaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self) -> None:
        self.storage: dict[int, ModelT] = {}
        self._next_id = 1

    def get_by_id(self, id: int) -> ModelT | None:
        return self.storage.get(id)

    def get_or_raise(self, id: int) -> ModelT:
        instance = self.get_by_id(id)
        if not instance:
            raise NotFoundError(f'{self.model.__name__} with ID {id} not found')
        return instance

    def update(self, id: int, **kwargs: Any) -> ModelT:
        instance = self.get_or_raise(id)

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance

    def create(self, **kwargs: Any) -> ModelT:
        instance = self.model(**kwargs)

        instance.id = self._next_id

        self.storage[instance.id] = instance

        self._next_id += 1
        return instance

    def delete(self, id: int) -> None:
        self.storage.pop(id)

    def list(
        self,
        *filters: Any,
        offset: int = 0,
        limit: int = 20,
    ) -> list[ModelT]:
        users = self.storage.copy()

        return list(users.values())

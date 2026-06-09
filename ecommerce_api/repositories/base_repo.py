from typing import Any, Generic, Protocol, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Mapped, Session
from ecommerce_api.core.exceptions import NotFoundError

class MappedModel(Protocol):
    __tablename__: str
    id: Mapped[int]


ModelT = TypeVar('ModelT', bound=MappedModel)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> ModelT | None:
        result = self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    def get_or_raise(self, id: int) -> ModelT:
        instance = self.get_by_id(id)
        if not instance:
            raise NotFoundError(f'{self.model.__name__} with id={id} not found')
        return instance

    def list(
        self,
        *filters: Any,
        offset: int = 0,
        limit: int = 20,
    ) -> list[ModelT]:
        result = self.session.execute(
            select(self.model).where(*filters).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    def create(self, **kwargs: Any) -> ModelT:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()  # gets the DB-assigned id without committing
        self.session.refresh(instance)
        return instance

    def update(self, id: int, **kwargs: Any) -> ModelT:
        self.session.execute(
            update(self.model).where(self.model.id == id).values(**kwargs)
        )
        return self.get_or_raise(id)

    def delete(self, id: int) -> None:
        self.session.execute(delete(self.model).where(self.model.id == id))

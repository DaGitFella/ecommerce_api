from sqlalchemy import func, select

from ecommerce_api.infrastructure.repositories.base import BaseRepository
from ecommerce_api.users.models import User
from ecommerce_api.users.schema import UserCreate


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_email(self, email: str) -> User | None:
        result = self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    def email_exists(self, email: str) -> bool:
        result = self.session.execute(select(func.count()).where(User.email == email))
        return result.scalar_one() > 0

    def list_active(self, offset: int = 0, limit: int = 20) -> list[User]:
        return self.list(User.is_active, offset=offset, limit=limit)

    def create_user(self, data: UserCreate) -> User:
        return self.create(
            name=data.name, email=data.email, password_hash=data.password
        )

    def deactivate(self, id: int) -> User:
        return self.update(id=id, is_active=False)

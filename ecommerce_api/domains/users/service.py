from ecommerce_api.core.events.bus import EventBus
from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.core.security.password_hasher import PasswordHasher

from .events import UserRegistered
from .models import User
from .repository import UserRepository
from .schema import UserCreate, UserList, UserUpdate


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hash: PasswordHasher,
        event_bus: EventBus,
    ) -> None:
        self.repo = user_repo
        self.event_bus = event_bus
        self.password_hash = password_hash

    async def register(self, data: UserCreate) -> User:
        if self.repo.email_exists(data.email):
            raise ConflictError(f'Email {data.email} already taken.')

        hashed_password = self.password_hash.get_password_hash(data.password)

        user = self.repo.create_user(data, hashed_password)

        await self.event_bus.publish(UserRegistered(user=user, email=user.email))

        return user

    def deactivate_user(self, id: int):
        self.repo.get_or_raise(id)
        return self.repo.deactivate(id)

    def update_user(self, id: int, data: UserUpdate) -> User:
        if self.repo.email_exists(data.email):
            raise ConflictError(f'Email {data.email} already taken.')

        return self.repo.update(id=id, **data.model_dump())

    def delete_user(self, id: int) -> None:
        user = self.repo.get_or_raise(id=id)

        return self.repo.delete(user.id)

    def get_user_by_id(self, id: int) -> User:
        return self.repo.get_or_raise(id)

    def get_user_by_email(self, email: str) -> User:
        user = self.repo.get_by_email(email)
        if not user:
            raise NotFoundError(detail=f'user with email {email} not found')

        return user

    def list_users(self, offset: int = 0, limit: int = 20, *filters: any) -> UserList:
        users = self.repo.list(offset=offset, limit=limit, *filters)
        return {'users': users}

    def list_active_users(self, offset: int = 0, limit: int = 20) -> UserList:
        users = self.repo.list_active()

        return {'users': users}

    def list_deactived_users(self, limit: int = 20, offset: int = 0) -> UserList:
        users = self.repo.list_deactive(offset=offset, limit=limit)

        return {'users': users}

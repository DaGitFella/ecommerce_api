from ecommerce_api.models import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate, UserUpdate


class FakeUserRepo(UserRepository):
    def __init__(self):
        self._next_id = 1
        self.users = {}

    def email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self.users.values())

    def get_by_id(self, id: int) -> User | None:
        try:
            user = self.users[id]

            return user
        except KeyError:
            return None

    def get_or_raise(self, id: int) -> User:
        return super().get_or_raise(id)

    def create_user(self, data: UserCreate) -> User:
        user = User(email=data.email, name=data.name, password_hash=data.password)

        user.id = self._next_id

        self.users[user.id] = user

        self._next_id += 1
        return user

    def update(self, id: int, **kwargs) -> User:
        db_user: User = self.get_or_raise(id)

        data = UserUpdate.model_validate(kwargs)

        update_dict = data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        return db_user

    def delete(self, id: int) -> None:
        self.users.pop(id)

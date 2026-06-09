from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.models.users import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register(self, data: UserCreate) -> User:
        if self.repo.email_exists(data.email):
            raise ConflictError(f'Email {data.email} already taken.')
        hashed_password = data.password
        return self.repo.create_user(data, hashed_password)

    def deactivate(self, id: int) -> User:
        return self.repo.update(id=id, is_active=False)

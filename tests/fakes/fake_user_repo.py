from typing import Any

from ecommerce_api.models import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate


class FakeUserRepo(UserRepository):
    def __init__(self):
        self.users = {}

    def email_exists(self, email: str) -> bool:
        return email in self.users

    def create_user(self, data: UserCreate) -> User:
        user = User(email=data.email, name=data.name, password_hash=data.password)
        self.users[data.email] = user
        return user
    
    def update(self, id: int, **kwargs) -> User:
        return super().update(id, **kwargs)

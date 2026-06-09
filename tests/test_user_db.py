import pytest

from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.models.users import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate
from ecommerce_api.services.user_services import UserService


class FakeUserRepo(UserRepository):
    def __init__(self):
        self.users = {}

    def email_exists(self, email: str) -> bool:
        return email in self.users

    def create_user(self, data, hashed_password):
        user = User(email=data.email, name='teste', password_hash='senha123')
        self.users[data.email] = user
        return user


def test_register_user_must_return_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        repo = UserRepository(session)

        service = UserService(repo)

        user = UserCreate(email='user@example.com', name='user', password='senha123')

        db_user = service.register(user)

        assert db_user.id == 1
        assert db_user.name == 'user'
        assert db_user.password_hash == 'senha123'
        assert db_user.created_at == time


def test_create_user_must_return_409():
    repo = FakeUserRepo()
    repo.users['taken@email.com'] = True

    service = UserService(repo)

    with pytest.raises(ConflictError):
        service.register(
            UserCreate(email='taken@email.com', name='taken', password='senha123')
        )


def test_deactivate_user(session, user):
    repo = UserRepository(session)

    service = UserService(repo)

    db_user = service.deactivate(id=1)

    assert not db_user.is_active

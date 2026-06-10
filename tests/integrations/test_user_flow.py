import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.models.users import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate, UserUpdate
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

    with pytest.raises(ConflictError):  # assert when the method returns an raise
        service.register(
            UserCreate(email='taken@email.com', name='taken', password='senha123')
        )


def test_deactivate_user(session, user):
    repo = UserRepository(session)

    service = UserService(repo)

    db_user = service.deactivate(id=1)

    assert not db_user.is_active


def test_deactivate_unavaible_user_must_return_value_error(session):
    repo = UserRepository(session)

    service = UserService(repo)

    with pytest.raises(NotFoundError, match='User with id=2 not found'):
        service.deactivate(id=2)


def test_update_user_must_return_user(session, user):
    repo = UserRepository(session)

    service = UserService(repo)

    update_data = UserUpdate(
        name='claudio',
        email='claudio@gmail.com',
    )

    user = service.update_user(id=user.id, data=update_data)

    assert user.name == update_data.name
    assert user.email == update_data.email


def test_update_user_must_return_conflict(session, user, user_two):
    repo = UserRepository(session)

    service = UserService(repo)

    update_data = UserUpdate(name='test', email='test@test.com')

    with pytest.raises(ConflictError, match='Email test@test.com already taken.'):
        service.update_user(id=user_two.id, data=update_data)

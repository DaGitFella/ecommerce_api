import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.schemas.user_schema import UserCreate, UserUpdate


def test_create_user_must_return_409(user_service_with_users):
    service = user_service_with_users

    with pytest.raises(ConflictError):  # assert when the method returns an raise
        service.register(
            UserCreate(email='taken@email.com', name='taken', password='senha123')
        )


def test_create_user_must_return_user(user_service):
    service = user_service

    db_user = UserCreate(
        name='bernardo', email='bernando@example.com', password='senhadobernardo'
    )

    user = service.register(db_user)

    assert user.email == db_user.email
    assert user.name == db_user.name
    assert user.password_hash == db_user.password


def test_update_user_must_return_user(user_service_with_users):
    service = user_service_with_users

    update_data = UserUpdate(name='Claudio', email='bernado@example.com')

    user = service.update_user(data=update_data, id=1)

    assert user.id == 1
    assert user.email == update_data.email
    assert user.name == update_data.name


def test_update_user_must_return_not_found(user_service_with_users):
    service = user_service_with_users

    update_data = UserUpdate(name='Claudio', email='bernado@example.com')

    with pytest.raises(NotFoundError):
        service.update_user(data=update_data, id=3)


def test_update_user_must_return_conflict(user_service_with_users):
    service = user_service_with_users

    update_data = UserUpdate(name='Claudio', email='taken@email.com')

    with pytest.raises(ConflictError):
        service.update_user(data=update_data, id=2)


def test_delete_user_must_return_none(user_service_with_users):
    service = user_service_with_users

    user = service.repo.get_by_id(1)

    result = service.delete_user(user.id)

    assert result is None


def test_delete_user_must_return_not_found(user_service):
    service = user_service

    with pytest.raises(NotFoundError):
        service.delete_user(id=1)


def test_get_user_must_return_user(user_service_with_users):
    service = user_service_with_users

    user = service.repo.get_or_raise(1)

    assert hasattr(user, 'email')
    assert hasattr(user, 'password_hash')
    assert hasattr(user, 'id')
    assert hasattr(user, 'name')


def test_get_user_must_return_not_found(user_service):
    service = user_service

    with pytest.raises(NotFoundError):
        service.repo.get_or_raise(id=1)


def test_get_users_must_return_user_list(user_service_with_users):
    service = user_service_with_users

    users = service.repo.list()

    assert isinstance(users, list)
    assert {user.email for user in users} == {
        'taken@email.com',
        'email@example.com',
    }
    assert {user.name for user in users} == {'taken', 'usuario'}
    assert [user.id for user in users] == [1, 2]

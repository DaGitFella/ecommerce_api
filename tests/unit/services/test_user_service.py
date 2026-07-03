import pytest

from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.users.schema import UserCreate, UserUpdate


def test_create_user_must_return_409(fake_user_service_with_users):
    service = fake_user_service_with_users

    with pytest.raises(ConflictError):  # assert when the method returns an raise
        service.register(
            UserCreate(email='taken@email.com', name='taken', password='senha123')
        )


def test_create_user_must_return_user(fake_user_service_with_users):
    service = fake_user_service_with_users

    db_user = UserCreate(
        name='bernardo', email='bernando@example.com', password='senhadobernardo'
    )

    user = service.register(db_user)

    assert user.email == db_user.email
    assert user.name == db_user.name
    assert user.password_hash == db_user.password


def test_update_user_must_return_user(fake_user_service_with_users):
    service = fake_user_service_with_users

    update_data = UserUpdate(name='Claudio', email='bernado@example.com')

    user = service.update_user(data=update_data, id=1)

    assert user.id == 1
    assert user.email == update_data.email
    assert user.name == update_data.name


def test_update_user_must_return_not_found(fake_user_service_with_users):
    service = fake_user_service_with_users

    unreachable_id = 999

    update_data = UserUpdate(name='Claudio', email='bernado@example.com')

    with pytest.raises(NotFoundError):
        service.update_user(data=update_data, id=unreachable_id)


def test_update_user_must_return_conflict(fake_user_service_with_users):
    service = fake_user_service_with_users

    update_data = UserUpdate(name='Claudio', email='taken@email.com')

    with pytest.raises(ConflictError):
        service.update_user(data=update_data, id=2)


def test_delete_user_must_raise_not_found_if_deleted(fake_user_service_with_users):
    service = fake_user_service_with_users

    user_id = 1

    service.delete_user(user_id)

    with pytest.raises(NotFoundError):
        service.get_user_by_id(user_id)


def test_delete_user_must_return_not_found(fake_user_service_with_users):
    service = fake_user_service_with_users

    unreachable_id = 999

    with pytest.raises(NotFoundError):
        service.delete_user(id=unreachable_id)


def test_get_user_must_return_user(fake_user_service_with_users):
    service = fake_user_service_with_users

    user = service.get_user_by_id(1)

    assert hasattr(user, 'email')
    assert hasattr(user, 'password_hash')
    assert hasattr(user, 'id')
    assert hasattr(user, 'name')


def test_get_user_must_return_not_found(fake_user_service_with_users):
    service = fake_user_service_with_users

    unreachable_id = 999

    with pytest.raises(NotFoundError):
        service.get_user_by_id(id=unreachable_id)


def test_get_users_must_return_user_list(fake_user_service_with_users):
    service = fake_user_service_with_users

    user_list = service.list_users()

    assert isinstance(user_list, dict)
    assert {user.email for user in user_list['users']} == {
        'taken@email.com',
        'email@example.com',
        'deactive@example.com',
    }
    assert {user.name for user in user_list['users']} == {
        'taken',
        'usuario',
        'deactivated',
    }
    assert [user.id for user in user_list['users']] == [1, 2, 3]


def test_deactivate_user_must_return_user(fake_user_service_with_users):
    service = fake_user_service_with_users

    user = service.deactivate_user(id=1)

    assert user.is_active is False


def test_deactivate_user_must_return_not_found_error(fake_user_service_with_users):
    service = fake_user_service_with_users

    unreachable_id = 999

    with pytest.raises(NotFoundError):
        service.deactivate_user(unreachable_id)


def test_list_active_user_must_return_active_users_list(fake_user_service_with_users):
    service = fake_user_service_with_users

    active_users = service.list_active_users()

    assert 'users' in active_users
    assert len(active_users['users']) > 0

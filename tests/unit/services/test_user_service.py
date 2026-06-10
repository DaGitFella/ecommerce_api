import pytest

from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.schemas.user_schema import UserCreate, UserUpdate


def test_create_user_must_return_409(user_service_with_user):
    service = user_service_with_user

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

def test_update_user_must_return_user(user_service_with_user):
    service = user_service_with_user
    
    update_data = UserUpdate(name='Claudio', email='bernado')
    
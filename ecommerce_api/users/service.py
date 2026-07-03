from ecommerce_api.core.exceptions import ConflictError, NotFoundError
from ecommerce_api.shopping_carts.service import ShoppingCartService
from ecommerce_api.users.models import User
from ecommerce_api.users.repository import UserRepository
from ecommerce_api.users.schema import UserCreate, UserList, UserUpdate


class UserService:
    def __init__(
        self, user_repo: UserRepository, shopping_cart_service: ShoppingCartService
    ) -> None:
        self.repo = user_repo
        self.shopping_cart_service = shopping_cart_service

    def register(self, data: UserCreate) -> User:
        if self.repo.email_exists(data.email):
            raise ConflictError(f'Email {data.email} already taken.')
        # do hashing here
        user = self.repo.create_user(data)
        self.shopping_cart_service.create_default_shopping_cart(
            user=user
        )  # create default shopping cart for the user
        return user

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
        users = self.repo.list_active

        return {'users': users}

    def list_deactived_users(self, limit: int = 20, offset: int = 0) -> UserList:
        users = self.repo.list_deactive(offset=offset, limit=limit)

        return {'users': users}

from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.models.users import User
from ecommerce_api.repositories.user_repo import UserRepository
from ecommerce_api.schemas.user_schema import UserCreate, UserUpdate
from ecommerce_api.services.shopping_cart_service import ShoppingCartService


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

    def deactivate(self, id: int) -> User:
        return self.repo.update(id=id, is_active=False)

    def update_user(self, id: int, data: UserUpdate) -> User:
        if self.repo.email_exists(data.email):
            raise ConflictError(f'Email {data.email} already taken.')

        return self.repo.update(id=id, **data.model_dump())

    def delete_user(self, id: int) -> None:
        user = self.repo.get_or_raise(id=id)

        return self.repo.delete(user.id)

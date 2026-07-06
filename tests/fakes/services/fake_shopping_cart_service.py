from ecommerce_api.domains.users.models import User


class FakeCartService:
    def __init__(self) -> None:
        self.calls: list[User] = []

    async def create_default_shopping_cart(self, user: User) -> None:
        self.calls.append(user)

from ecommerce_api.models import User
from ecommerce_api.repositories.user_repo import UserRepository
from tests.fakes.fake_base_repo import FakeBaseRepository


class FakeUserRepo(FakeBaseRepository[User], UserRepository):
    def __init__(self):
        super().__init__()
        self.model = User

    def email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self.storage.values())

    def get_by_email(self, email: str) -> User | None:
        for id, instance in self.storage.items():
            if instance.email == email:
                user = instance
                return user

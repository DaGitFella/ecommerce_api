import typing

from ecommerce_api.core.security.password_hasher import PasswordHasher


class FakePasswordHasher(PasswordHasher):
    def __init__(self):
        self.password_context = 5381

    @typing.override
    def get_password_hash(self, plain_password: str) -> str:
        return f'hashed:{plain_password}'

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if self.get_password_hash(plain_password) == hashed_password:
            return True

        return False

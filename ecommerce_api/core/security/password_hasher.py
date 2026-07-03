from pwdlib import PasswordHash


class PasswordHasher:
    def __init__(self):
        self.password_context = PasswordHash.recommended()

    def get_password_hash(self, plain_password: str) -> str:
        return self.password_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

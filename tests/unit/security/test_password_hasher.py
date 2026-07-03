from ecommerce_api.core.security.password_hasher import PasswordHasher


def test_password_hasher_must_return_true_for_valid_password():
    plain_password = 'strong_password_ah'

    password_hash = PasswordHasher()

    hashed_password = password_hash.get_password_hash(plain_password)

    assert password_hash.verify_password(plain_password, hashed_password)


def test_password_hasher_must_return_false_for_invalid_password():
    plain_password = 'stron_password'

    password_hash = PasswordHasher()

    hashed_password = password_hash.get_password_hash(plain_password)

    assert not password_hash.verify_password('weak_password', hashed_password)

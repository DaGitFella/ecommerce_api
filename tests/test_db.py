from dataclasses import asdict

from sqlalchemy import select

from ecommerce_api.models.users import User, UserRole


def test_create_user_must_return_user_object(session, mock_db_time):
    with mock_db_time(User) as time:
        new_user = User(
            name='John Doe',
            email='johndoe@example.com',
            password_hash='hashedpassword',
            role=UserRole.CUSTOMER,
            profile_picture_url='http://example.com/profile.jpg',
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.email == 'johndoe@example.com'))

        assert asdict(user) == {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password_hash': 'hashedpassword',
            'role': UserRole.CUSTOMER,
            'profile_picture_url': 'http://example.com/profile.jpg',
            'created_at': time,
        }

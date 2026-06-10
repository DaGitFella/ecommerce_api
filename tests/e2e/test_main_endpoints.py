from http import HTTPStatus


def test_read_root_must_return_200_and_welcome_message(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to the E-commerce API!'}

from http import HTTPStatus


def test_get_users_must_return_200_and_random_message(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()


def test_create_user_must_return_201_and_random_message(client):
    response = client.post('/users')
    assert response.status_code == HTTPStatus.CREATED
    assert 'message' in response.json()


def test_update_user_must_return_202_and_random_message(client):
    response = client.put('/users/1')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert 'message' in response.json()


def test_delete_user_must_return_204(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not response.content


def test_get_user_must_return_200_and_random_message(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()

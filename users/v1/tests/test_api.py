import pytest

from starlette.testclient import TestClient
from server import app


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    yield client


def test_invalid_auth(client: TestClient):
    response = client.get('/v1/auth/', headers={'token': 'invalid'})
    assert response.status_code == 404


def test_user_register(client: TestClient):
    response = client.post('/v1/register/', json={
        'username': 'username',
        'password': 'password'
    })
    assert response.status_code == 200

    data = response.json()
    token = data['token']

    assert data.get('id') is not None
    assert data.get('username') == 'username'

    response = client.get('/v1/auth/', params={'token': token})
    assert response.status_code == 200

    data = response.json()
    assert data.get('username') == 'username'


def test_already_registered(client: TestClient):
    response = client.post('/v1/register/', json={
        'username': 'username',
        'password': 'password'
    })
    assert response.status_code == 400


def test_login(client: TestClient):
    response = client.post('/v1/login/', json={
        'username': 'username',
        'password': 'password'
    })
    assert response.status_code == 200

    data = response.json()
    token = data['token']

    assert data['username'] == 'username'

    response = client.get('/v1/auth/', params={'token': token})
    assert response.status_code == 200

    data = response.json()
    assert data.get('username') == 'username'


def test_logout(client: TestClient):
    response = client.post('/v1/login/', json={
        'username': 'username',
        'password': 'password'
    })
    assert response.status_code == 200

    user_id = response.json()['id']
    token = response.json()['token']

    response = client.delete('/v1/logout/', params={'user_id': user_id})
    assert response.status_code == 200

    response = client.get('/v1/auth/', params={'token': token})
    assert response.status_code == 404


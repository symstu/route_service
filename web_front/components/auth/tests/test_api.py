import uuid
import pytest

from starlette.testclient import TestClient


@pytest.fixture(scope='session')
def username():
    return str(uuid.uuid4())


def test_register_page(client: TestClient):
    response = client.get('/register/')
    assert response.status_code == 200


def test_register_missed_data(client: TestClient):
    response = client.post('/register/', data={'username': ''})
    assert response.status_code == 400


def test_register(client: TestClient, username):
    response = client.post('/register/', data={
        'username': username,
        'password': 'password',
        'password_confirmation': 'password'
    })
    assert response.status_code == 307
    assert response.cookies['session'] is not None


def test_register_again(client: TestClient, username):
    response = client.post('/register/', data={
        'username': username,
        'password': 'password',
        'password_confirmation': 'password'
    })
    assert response.status_code == 409


def test_login_page_get(client: TestClient):
    response = client.get('/login/')
    assert response.status_code == 200


def test_login_missed_data(client: TestClient):
    response = client.post('/login/', data={})
    assert response.status_code == 400


def test_login_invalid_data(client: TestClient):
    response = client.post('/login/', data={
        'username': 'podorizhnik',
        'password': 'pushystyi'
    })
    assert response.status_code == 404


def test_login(client: TestClient, username):
    response = client.post('/login/', data={
        'username': username,
        'password': 'password'
    })
    assert response.status_code == 307
    assert response.cookies['session'] is not None

    response = client.post('/logout/',
                           cookies={'session': response.cookies['session']})
    assert response.status_code == 303
    assert 'session' not in response.cookies

import pytest

from starlette.testclient import TestClient
from server import app


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    yield client


def test_create_route(client):
    response = client.put('/v1/routes/', json={
        'user_id': -1,
        'route_id': 0,
        'route_length': 1.0
    })
    assert response.status_code == 200
    assert response.json()['id'] is not None


def test_users_stats(client):
    response = client.get('/v1/stats/')
    assert response.status_code == 200
    assert response.json()

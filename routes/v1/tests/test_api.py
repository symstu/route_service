import pytest

from starlette.testclient import TestClient
from server import app


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    yield client


def test_list_of_points(client):
    response = client.get('/v1/points/')
    assert response.status_code == 200
    assert len(response.json())


def test_list_of_routes(client):
    response = client.get('/v1/routes/')
    assert response.status_code == 200
    assert len(response.json())


created_route_id = None


def test_gen_and_save_new(client):
    global created_route_id

    response = client.post('/v1/routes/', json={'start': 'A', 'finish': 'Z'})
    assert response.status_code == 200

    points_id = [point['id'] for point in response.json()]
    assert len(points_id) == 5

    response = client.put('/v1/routes/', json={
        'name': 'new_route_2',
        'points': points_id
    })
    assert response.status_code == 200
    assert response.json()['id'] is not None

    created_route_id = response.json()['id']


def test_routes_batch(client: TestClient):
    response = client.post('/v1/batch/', json={
        'routes_id': [created_route_id]})
    assert response.status_code == 200
    assert response.json()

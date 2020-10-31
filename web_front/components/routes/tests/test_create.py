import uuid

from starlette.testclient import TestClient


def test_unauth_generator(client: TestClient):
    response = client.get('/generator/')
    assert response.status_code == 200
    assert b'ONE ROUTE' in response.content


def test_generator(registered_user: TestClient):
    response = registered_user.get('/generator/')
    assert response.status_code == 200
    assert b'Start' in response.content


def test_generator_gen(registered_user: TestClient):
    response = registered_user.post('/generator/', data={
        'start': 'A',
        'finish': 'F'
    })
    assert response.status_code == 200


def test_save_route(registered_user: TestClient):
    response = registered_user.post('/generator/save/', data={
        'name': str(uuid.uuid4()),
        'points': '1-2-3-4'
    })
    assert response.status_code == 307
    assert response.headers['location'] == '/'

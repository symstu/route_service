from starlette.testclient import TestClient


def test_unauth_generator(client: TestClient):
    response = client.get('/stats/')
    assert response.status_code == 200
    assert b'ONE ROUTE' in response.content


def test_generator(registered_user: TestClient):
    response = registered_user.get('/stats/')
    assert response.status_code == 200

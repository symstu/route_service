from starlette.testclient import TestClient


def test_anon_routes(client: TestClient):
    response = client.get('/routes/')
    assert response.status_code == 200
    assert b'ONE ROUTE' in response.content


def test_routes(registered_user: TestClient):
    response = registered_user.get('/routes/')
    assert response.status_code == 200
    assert b'points' in response.content

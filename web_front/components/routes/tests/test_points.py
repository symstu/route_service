from starlette.testclient import TestClient


def test_anon_points(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ONE ROUTE' in response.content


def test_points(registered_user: TestClient):
    response = registered_user.get('/')
    assert response.status_code == 200
    assert b'lat' in response.content

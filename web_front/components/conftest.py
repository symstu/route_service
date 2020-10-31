import uuid
import asyncio
import pytest

from starlette.testclient import TestClient

from server import app


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
def client():

    client = TestClient(app)
    yield client


@pytest.fixture(scope='session')
def registered_user(client):
    new_uuid = str(uuid.uuid4())

    response = client.post('/register/', data={
        'username': new_uuid,
        'password': new_uuid,
        'password_confirmation': new_uuid
    })
    assert response.status_code == 307
    assert response.cookies['session'] is not None

    yield client

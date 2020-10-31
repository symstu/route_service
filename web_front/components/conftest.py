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

import asyncio
import pytest

from seeds import generate_points_and_routes


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
async def load_seeds():
    await generate_points_and_routes()

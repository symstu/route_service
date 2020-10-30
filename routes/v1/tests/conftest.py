import asyncio
import pytest


from seeds import generate_dots


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
async def create_dots():
    await generate_dots()


@pytest.fixture(scope='session', autouse=True)
async def create_routes():
    await generate_dots()

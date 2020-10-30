import pytest

from models import Points, RouteMeta


@pytest.mark.asyncio
async def test_points_list():
    data = await Points.list()
    assert len(data)


@pytest.mark.asyncio
async def test_list_of_routes():
    data = await RouteMeta.list()
    assert len(data) > 0

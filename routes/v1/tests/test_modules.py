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


@pytest.mark.asyncio
async def test_gen_and_save_new():
    data = await Points.list()
    point_a, point_b = data[:2]

    data = await RouteMeta.generate(point_a['id'], point_b['id'])
    assert len(data) == 5

    data = await RouteMeta.create('new_route', [item['id'] for item in data])
    assert len(data) == 5

    data = await RouteMeta.list()
    assert 'new_route' in data
    assert len(data['new_route']['points']) == 5

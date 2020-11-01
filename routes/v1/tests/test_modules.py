import pytest

from models import Points, RouteMeta


@pytest.mark.asyncio
async def test_points_list():
    data = await Points.list(0, 20)
    assert len(data)


@pytest.mark.asyncio
async def test_list_of_routes():
    data = await RouteMeta.list(0, 20)
    assert len(data) > 0


created_routes_id = None


@pytest.mark.asyncio
async def test_gen_and_save_new():
    global created_routes_id

    data = await Points.list(0, 20)
    point_a, point_b = data[:2]

    data = await RouteMeta.generate(point_a['name'], point_b['name'])
    assert len(data) == 5

    data = await RouteMeta.create('new_route', [item['id'] for item in data])
    assert len(data) == 5

    created_routes_id = data[0]['meta']

    data = await RouteMeta.list(0, 20)
    assert 'new_route' in data
    assert len(data['new_route']['points']) == 5


@pytest.mark.asyncio
async def test_get_batch():
    data = await RouteMeta.get_batch([created_routes_id])
    assert len(data)

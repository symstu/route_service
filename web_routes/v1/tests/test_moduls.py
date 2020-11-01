import pytest

from v1 import models


@pytest.mark.asyncio
async def test_create_routes():
    users_to_routs = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0),
    ]

    for user_id, route_id in users_to_routs:
        data = await models.UserRoutes.create(user_id, route_id)
        assert data is not None


@pytest.mark.asyncio
async def test_users_stats():
    stats = [
        (0, 1.0), (0, 2.0), (0, 3.0),
        (1, 2.0)
    ]

    ids = []

    for user_id, route_length in stats:
        data = await models.UserStats.add_user_route(user_id, route_length)
        assert data

        stats_id = data[0]['id']

        if stats_id not in ids:
            ids.append(stats_id)

    users_stats = await models.UserStats.stats(0, 15)

    def get_stat_by_id(stat_id):
        for index, i in enumerate(users_stats):
            if i['id'] == stat_id:
                return index
        raise ValueError

    stats_1, stats_2 = ids
    index_1 = get_stat_by_id(stats_1)
    index_2 = get_stat_by_id(stats_2)

    assert users_stats[index_1]['routes_amount'] == 3
    assert users_stats[index_1]['routes_length'] == 6.0

    assert users_stats[index_2]['routes_amount'] == 1
    assert users_stats[index_2]['routes_length'] == 2.0

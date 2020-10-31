import pytest

from v1 import models


@pytest.mark.asyncio
async def test_create_routes():
    users_to_routs = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 0),
    ]

    for user_id, route_id in users_to_routs:
        data = await models.UserRoutes.create(user_id, route_id)
        assert data is not None


@pytest.mark.asyncio
async def test_users_stats():
    stats = await models.UserRoutes.users_routes()

    assert stats[0] == [0, 1, 2, 3]
    assert stats[1] == [0]

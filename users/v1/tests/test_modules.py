import uuid
import pytest

from v1 import exc
from v1.models import User


@pytest.mark.asyncio
async def test_user_auth():
    with pytest.raises(exc.UserNotFound):
        result = await User.login('invalid_username', 'password')
        assert result is None

    new_username = str(uuid.uuid4())
    user_session = (await User.register(new_username, 'password'))['token']
    assert user_session is not None

    result = await User.authorize(new_username, 'password')
    assert result is not None

    user = await User.authenticate(user_session)
    assert user.get('username') == new_username

    result = await User.logout(user.get('id'))
    assert result is not None

    result = await User.logout(user.get('id'))
    assert result is None


@pytest.mark.asyncio
async def test_get_users_batch():
    user = await User.register(str(uuid.uuid4()), 'password')
    users = await User.get_batch([user['id']])
    assert len(users)

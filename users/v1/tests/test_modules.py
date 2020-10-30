import pytest

from v1 import exc
from v1.models import User


@pytest.mark.asyncio
async def test_user_auth():
    with pytest.raises(exc.UserNotFound):
        result = await User.login('invalid_username', 'password')
        assert result is None

    user_session = await User.register('username', 'password')
    assert user_session is not None

    result = await User.authorize('username', 'password')
    assert result is not None

    user = await User.authenticate(user_session)
    assert user.get('username') == 'username'

    result = await User.logout(user.get('id'))
    assert result is not None

    result = await User.logout(user.get('id'))
    assert result is None

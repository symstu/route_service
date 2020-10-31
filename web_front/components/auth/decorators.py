import typing

from starlette.requests import Request
from starlette.responses import RedirectResponse

from components.auth.client import UsersClient


def only_authorized():
    def wrapper(method: typing.Coroutine):
        async def wrapped(view_class, request: Request):
            user_token = request.cookies.get('session')

            if not user_token:
                return RedirectResponse('/login/')

            async with UsersClient() as client:
                user = await client.get_by_token(user_token)

            if not user:
                return RedirectResponse('/login/')

            return await method(view_class, request, user=user)

        return wrapped
    return wrapper

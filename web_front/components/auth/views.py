from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates

from components.auth.inputs import LoginForm, RegisterForm
from components.auth.client import UsersClient
from components.auth.decorators import only_authorized


templates = Jinja2Templates('')


class LoginPage(HTTPEndpoint):
    async def get(cls, request: Request):
        return templates.TemplateResponse(
            'components/auth/templates/login.html',
            {'request': request}
        )

    async def post(cls, request: Request):
        try:
            form = LoginForm(**await request.form())
        except Exception:
            return templates.TemplateResponse(
                'components/auth/templates/login.html',
                {'request': request, 'error': 'Invalid data'},
                status_code=400
            )

        async with UsersClient() as client:
            user = await client.login(form.username, form.password)

        if not user:
            return templates.TemplateResponse(
                'components/auth/templates/login.html',
                {'request': request, 'error': 'User not found'},
                status_code=404
            )

        return RedirectResponse(
            url='/', headers={'session': user.pop('token')})


class RegisterPage(HTTPEndpoint):
    async def get(cls, request):
        return templates.TemplateResponse(
            'components/auth/templates/register.html',
            {'request': request}
        )

    async def post(cls, request: Request):
        data = await request.form()

        try:
            form = RegisterForm(**data)
        except Exception:
            return templates.TemplateResponse(
                'components/auth/templates/register.html',
                {'request': request, 'error': 'Missed data'},
                status_code=400
            )

        if not form.password or not form.username:
            return templates.TemplateResponse(
                'components/auth/templates/register.html',
                {'request': request, 'error': 'Invalid data'},
                status_code=400
            )

        if form.password != form.password_confirmation:
            return templates.TemplateResponse(
                'components/auth/templates/register.html',
                {'request': request, 'error': 'Different passwords'},
                status_code=400
            )

        async with UsersClient() as client:
            user = await client.register(form.username, form.password)

        if not user:
            return templates.TemplateResponse(
                'components/auth/templates/register.html',
                {'request': request,
                 'error': 'User with such email already registered'},
                status_code=409
            )

        return RedirectResponse(
            url='/', headers={'session': user.pop('token')})


class LogoutPage(HTTPEndpoint):

    @only_authorized()
    async def post(cls, _, user=None):
        async with UsersClient() as client:
            await client.logout(user['id'])

        return RedirectResponse(url='/login/', headers={})


routes = [
    Route('/login/', LoginPage),
    Route('/register/', RegisterPage),
    Route('/logout/', LogoutPage),
]

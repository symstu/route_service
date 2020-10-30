from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.schemas import SchemaGenerator

from v1 import inputs, models, exc


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "SSO", "version": "1.0"}}
)


class AuthenticateView(HTTPEndpoint):
    async def get(self, request: Request):
        """
        responses:
            200:
                description: Get user by token.
                examples:
                    {"id": "0", "username": "john"}
            404:
                description: Token is invalid or expired
        """
        user_token = request.query_params.get('token')

        try:
            user = await models.User.authenticate(user_token)
            return JSONResponse(user)

        except exc.InvalidToken:
            return JSONResponse(status_code=404,
                                content={'message': 'Token is invalid or expired'})


class LoginView(HTTPEndpoint):
    async def post(self, request):
        """
        responses:
            200:
                description: Get user by username and password.
                examples:
                    {"id": "0", "username": "john"}
            404:
                description: User with such credentials not found
        """
        data = inputs.LoginInput(**await request.json())

        try:
            user, session = await models.User.login(
                data.username, data.password)
            return JSONResponse(user, headers={'token': session})

        except exc.UserNotFound:
            return JSONResponse(status_code=404,
                                content={'message': 'User not found'})


class RegisterView(HTTPEndpoint):
    async def post(self, request):
        """
        responses:
            200:
                description: Register user with username and password.
                examples:
                    {"id": "0", "username": "john"}
            400:
                description: User with such name already exists
        """
        data = inputs.LoginInput(**await request.json())

        try:
            user, session = await models.User.register(
                data.username, data.password)
            return JSONResponse(user, headers={'token': session})

        except exc.UserAlreadyExists:
            return JSONResponse(status_code=400,
                                content={'message': 'Username already exists'})


class LogoutView(HTTPEndpoint):
    """
    responses:
        200:
            description: Register user with username and password.
        400:
            description: User with such name already exists
    """
    async def delete(cls, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return JSONResponse(status_code=404,
                                content={'message': 'User not found'})

        await models.User.logout(int(user_id))
        return JSONResponse(status_code=200)


def open_api_schema(request: Request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route('/v1/register/', RegisterView),
    Route('/v1/login/', LoginView),
    Route('/v1/auth/', AuthenticateView),
    Route('/v1/logout/', LogoutView),

    Route('/schema', endpoint=open_api_schema, include_in_schema=False)
]

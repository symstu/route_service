from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.schemas import SchemaGenerator

from v1 import inputs, models


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Routes", "version": "1.0"}}
)


class RouteCreateView(HTTPEndpoint):
    async def put(cls, request):
        data = inputs.CreateUserRouteInput(**await request.json())

        created_route = await models.UserRoutes.create(
            data.user_id, data.route_id)
        return JSONResponse({'id': created_route[0]['id']})


class UsersStatsView(HTTPEndpoint):
    async def get(cls, _):
        return JSONResponse(await models.UserRoutes.users_routes())


def open_api_schema(request: Request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route('/v1/routes/', RouteCreateView),
    Route('/v1/stats/', UsersStatsView),

    Route('/schema', endpoint=open_api_schema, include_in_schema=False)
]

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.schemas import SchemaGenerator

import models
from v1 import inputs


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Routes", "version": "1.0"}}
)


class PointsView(HTTPEndpoint):
    async def get(cls, _):
        """
        responses:
            200:
                description: Get user by token.
                examples:
                    {"id": "0", "username": "john"}
        """
        data = await models.Points.list()
        serialized = [{'id': item['id'],
                       'name': item['name'],
                       'lat': item['lat'],
                       'lon': item['lon']} for item in data]
        return JSONResponse(serialized)


class RoutesView(HTTPEndpoint):
    async def get(cls, _):
        """
        responses:
            200:
                description: Get all routes.
                examples:
                    {"id": "0", "username": "john"}
        """
        return JSONResponse(await models.RouteMeta.list())

    async def post(cls, request: Request):
        """
        responses:
            200:
                description: generate new route.
                examples:
                    [{"id": "0", "name": "A"}]
        """

        data = inputs.GenRouteInput(**await request.json())

        if not data.start or not data.finish:
            return JSONResponse(status_code=400, content=b'Missed points')

        created_route = await models.RouteMeta.generate(
            data.start, data.finish)
        return JSONResponse([{'id': item['id'], 'name': item['name']}
                             for item in created_route])

    async def put(cls, request: Request):
        """
        responses:
            200:
                description: create new route.
                examples:
                    {"id": "0", "username": "john"}
        """
        data = inputs.CreateRouteInput(**await request.json())

        if not data.name:
            return JSONResponse(status_code=400, content=b'Missed name')

        if len(data.points) < 3:
            return JSONResponse(status_code=400,
                                content=b'At least 3 dots have to be provided')

        data = await models.RouteMeta.create(data.name, data.points)
        return JSONResponse({'id': data[0]['meta']})


def open_api_schema(request: Request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route('/v1/points/', PointsView),
    Route('/v1/routes/', RoutesView),

    Route('/schema', endpoint=open_api_schema, include_in_schema=False)
]

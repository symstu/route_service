from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.schemas import SchemaGenerator

import models


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
        return JSONResponse(content=data)


class RoutesView(HTTPEndpoint):
    async def get(cls, _):
        """
        responses:
            200:
                description: Get all routes.
                examples:
                    {"id": "0", "username": "john"}
        """
        data = await models.RouteMeta.list()

    async def post(cls, request: Request):
        """
        responses:
            200:
                description: generate new route.
                examples:
                    {"id": "0", "username": "john"}
        """

    async def put(cls, request: Request):
        """
        responses:
            200:
                description: create new route.
                examples:
                    {"id": "0", "username": "john"}
        """


def open_api_schema(request: Request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route('/v1/points/', PointsView),
    Route('/v1/routes/', RoutesView),

    Route('/schema', endpoint=open_api_schema, include_in_schema=False)
]

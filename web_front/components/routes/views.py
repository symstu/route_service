from starlette.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates

from components.auth.decorators import only_authorized
from components.routes.client import RoutesClient, UserRoutesClient
from components.routes.inputs import GenerateRouteInput, SaveRouteInput


templates = Jinja2Templates('')


class PointsListPage(HTTPEndpoint):

    @only_authorized()
    async def get(cls, request, user):
        async with RoutesClient() as client:
            points = await client.points()

        return templates.TemplateResponse(
            'components/routes/templates/points.html',
            {'request': request, 'user': user, 'points': points}
        )


class RoutesListPage(HTTPEndpoint):

    @only_authorized()
    async def get(cls, request, user):
        async with RoutesClient() as client:
            created_routes = await client.routes()

        return templates.TemplateResponse(
            'components/routes/templates/routes.html',
            {'request': request, 'user': user, 'routes': created_routes}
        )


class RouteCreatePage(HTTPEndpoint):

    @only_authorized()
    async def get(cls, request, user):
        return templates.TemplateResponse(
            'components/routes/templates/create.html',
            {'request': request, 'user': user, 'point': None}
        )

    @only_authorized()
    async def post(self, request, user):
        try:
            form = GenerateRouteInput(**await request.form())
        except Exception:
            return templates.TemplateResponse(
                'components/routes/templates/create.html',
                {'request': request, 'user': user, 'point': None}
            )

        if not form.start or not form.finish:
            return templates.TemplateResponse(
                'components/routes/templates/create.html',
                {'request': request, 'user': user, 'point': None,
                 'error': 'Error: empty fields'}
            )

        async with RoutesClient() as client:
            points = await client.gen_route(
                form.start.upper(), form.finish.upper())

        if not points:
            return templates.TemplateResponse(
                'components/routes/templates/create.html',
                {'request': request, 'user': user, 'point': None,
                 'error': 'Error: Can not find entered points in DB'}
            )
        name = '-'.join([item['name'] for item in points])
        ids = '-'.join([str(item['id']) for item in points])

        return templates.TemplateResponse(
            'components/routes/templates/create.html',
            {'request': request, 'user': user, 'name': name, 'ids': ids}
        )


class GeneratorSave(HTTPEndpoint):

    @only_authorized()
    async def post(self, request, user):
        try:
            form = SaveRouteInput(**await request.form())
        except Exception:
            return RedirectResponse('/generator/')

        points = list(map(int, form.points.split('-')))

        async with RoutesClient() as client:
            new_route = await client.save_route(form.name, points)

        async with UserRoutesClient() as client:
            await client.create_route(
                user['id'], new_route['id'])

        return RedirectResponse('/')


class RouteStatsPage(HTTPEndpoint):

    @only_authorized()
    async def get(cls, _, __):
        async with UserRoutesClient() as client:
            data = await client.users_stats()

        users = [item['user_id'] for item in data]
        routes = [item['route_id'] for item in data]




routes = [
    Route('/', PointsListPage),
    Route('/routes/', RoutesListPage),
    Route('/stats/', RouteStatsPage),
    Route('/generator/', RouteCreatePage),
    Route('/generator/save/', GeneratorSave)
]

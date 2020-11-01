from starlette.responses import RedirectResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates

from components.auth.decorators import only_authorized
from components.auth.client import UsersClient
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
            return RedirectResponse('/generator/', status_code=303)

        points = list(map(int, form.points.split('-')))

        async with RoutesClient() as client:
            new_route = await client.save_route(form.name, points)
            route_points = await client.routes_batch([new_route['id']])

        fetched_points = route_points[str(new_route['id'])]['points']
        route_length = sum([(point['lat']+point['lon'])/2
                            for point in fetched_points])

        async with UserRoutesClient() as client:
            await client.create_route(
                user['id'], new_route['id'], route_length)

        return RedirectResponse('/', status_code=303)


class RouteStatsPage(HTTPEndpoint):

    @only_authorized()
    async def get(cls, request: Request, user):
        async with UserRoutesClient() as client:
            stats = await client.users_stats()

        users = [item['user_id'] for item in stats]

        async with UsersClient() as client:
            fetched_users = await client.batch_users(users)

        output = []

        for stat in stats:
            user_id = str(stat['user_id'])

            if user_id not in fetched_users:
                continue

            output.append({
                'id': stat['id'],
                'user': fetched_users[user_id]['username'],
                'total': stat['total'],
                'length': stat['length'],
            })

        return templates.TemplateResponse(
            'components/routes/templates/stats.html',
            {'request': request, 'user': user, 'stats': output}
        )


routes = [
    Route('/', RouteStatsPage),
    Route('/points/', PointsListPage),
    Route('/routes/', RoutesListPage),
    Route('/generator/', RouteCreatePage),
    Route('/generator/save/', GeneratorSave)
]

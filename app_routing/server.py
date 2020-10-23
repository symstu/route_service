from starlette.routing import Route
from starlette.endpoint import HTTPEndpoint

from config import templates


class DotesView(HTTPEndpoint):
    async def get(self, request):
        """
        Get list of available dots
        """
        return templates.TemplateResponse('index.html')

    async def put(self, request):
        """
        Create new dot
        """
        pass


class RoutesView(HTTPEndpoint):
    async def get(self, request):
        """
        Get list of all routes
        """
        pass

    async def post(self, request):
        """
        Create new route
        """
        pass

    async def put(self, request):
        """
        Save new route
        """
        pass


class RouteStatsView(HTTPEndpoint):
    async def get(self, request):
        """
        Get statistic about created routes and their length
        """
        pass


routes = [
    Route('/', DotesView),
    Route('/routes', RoutesView),
    Route('/stats', RouteStatsView),
]

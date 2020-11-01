import typing
import httpx

from config import conf


class RoutesClient(httpx.AsyncClient):
    def __init__(self):
        super(RoutesClient, self).__init__(base_url=conf.routes_url)

    async def points(self):
        response = await self.get(f'/v1/points/')
        return response.json()

    async def routes(self):
        response = await self.get('/v1/routes/')
        return response.json()

    async def gen_route(self, start: int, finish: int):
        response = await self.post('/v1/routes/', json={
            'start': start,
            'finish': finish
        })

        if response.status_code != 200:
            return

        return response.json()

    async def save_route(self, name: str, points: typing.List[int]):
        response = await self.put('/v1/routes/', json={
            'name': name,
            'points': points
        })
        return response.json()

    async def routes_batch(self, routes_id: typing.List[int]):
        response = await self.post('/v1/batch/', json={'routes_id': routes_id})
        return response.json()


class UserRoutesClient(httpx.AsyncClient):
    def __init__(self):
        super(UserRoutesClient, self).__init__(base_url=conf.web_routes_url)

    async def create_route(self, user_id: int, route_id: int, length: float):
        response = await self.put('/v1/routes/', json={
            'user_id': user_id,
            'route_id': route_id,
            'route_length': length
         })

        return response.json()

    async def users_stats(self):
        response = await self.get('/v1/stats/')
        return response.json()

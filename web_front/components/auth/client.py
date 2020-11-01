import httpx
import typing

from config import conf


class UsersClient(httpx.AsyncClient):
    def __init__(self):
        super(UsersClient, self).__init__(base_url=conf.users_url)

    async def login(self, username: str, password: str):
        response = await self.post(f'/v1/login/', json={
            'username': username,
            'password': password
        })

        if response.status_code == 404:
            return

        return response.json()

    async def register(self, username: str, password: str):
        response = await self.post('/v1/register/', json={
            'username': username,
            'password': password
        })

        if response.status_code == 400:
            return

        return response.json()

    async def get_by_token(self, token: str):
        response = await self.get('/v1/auth/', params={'token': token})

        if response.status_code == 404:
            return

        return response.json()

    async def logout(self, user_id: int):
        response = await self.delete('/v1/logout/', params={
            'user_id': user_id
        })

        if response.status_code == 404:
            return

        return response.json()

    async def batch_users(self, users_id: typing.List[int]):
        response = await self.post('/v1/batch/', json={'users_id': users_id})
        return response.json()

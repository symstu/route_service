import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from config import conf

Base = declarative_base()


class UserRoutes(Base):
    __tablename__ = 'user_routes'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    route_id = sa.Column(sa.Integer, nullable=False)

    @classmethod
    async def create(cls, user_id: int, route_id: int):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        INSERT INTO user_routes (user_id, route_id)
        VALUES ($1, $2)
        RETURNING id
        ''')
        return await request.fetch(user_id, route_id)

    @classmethod
    async def users_routes(cls):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            *
        FROM user_routes
        ''')
        routes = await request.fetch()
        users = {}

        for route in routes:
            user_id = route['user_id']

            if user_id not in users:
                users[user_id] = []

            users[user_id].append(route['route_id'])

        return users

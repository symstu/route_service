import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from config import conf

Base = declarative_base()


class UserStats(Base):
    __tablename__ = 'user_stats'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, nullable=False, unique=True)
    routes_amount = sa.Column(sa.Integer, nullable=False, server_default='0')
    routes_length = sa.Column(sa.Float, nullable=False, server_default='0.0')

    @classmethod
    async def add_user_route(cls, user_id: int, route_length: float):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        INSERT INTO user_stats (user_id, routes_amount, routes_length)
        VALUES ($1, 1, $2)
        ON CONFLICT (user_id) DO
            UPDATE SET 
                routes_amount = user_stats.routes_amount + 1,
                routes_length = user_stats.routes_length + EXCLUDED.routes_length
            WHERE user_stats.user_id = $1
        RETURNING id
        ''')
        return await request.fetch(user_id, route_length)

    @classmethod
    async def stats(cls):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            * 
        FROM user_stats
        ORDER BY id
        ''')
        return await request.fetch()


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

import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from config import conf

Base = declarative_base()


class Points(Base):
    __tablename__ = 'points'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    lat = sa.Column(sa.Float, nullable=False)
    lon = sa.Column(sa.Float, nullable=False)

    @classmethod
    async def list(cls):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT name, lat, lon FROM points
        ''')
        return await request.fetch()

    @classmethod
    async def create_many(cls, points):
        conn = await conf.db_conn()
        query = '''
            INSERT INTO points (name, lat, lon) 
            VALUES($1, $2, $3)
        '''
        await conn.executemany(query, points)


class RouteMeta(Base):
    __tablename__ = 'routes_meta'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

    @classmethod
    async def list(cls):
        """
        Get list of created points

        :return: list of points
        """
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            rm.id, 
            rm.name,
            p.name, 
            p.lat,
            p.lon
        FROM routes_meta rm
        JOIN routes r ON r.meta = rm.id
        JOIN points p ON r.point = p.id
        ORDER BY r.sequence
        ''')
        return await request.fetch()

    async def create_many(cls, name, routes):
        conn = await conf.db_conn()

        request = await conn.prepare(
            'INSERT INTO routes_meta (name) '
            'VALUES ($1) RETURNING id')

        new_route_id = await conn.fetch(request, name)

        await conn.executemany(
            'INSERT INTO routes (point, meta, sequence)'
            ' VALUES ($1, $2, $3)', routes)

    @classmethod
    async def get(cls, start: int, finish: int):
        pass

    @classmethod
    async def create(cls, start: int, finish: int):
        pass


class Routes(Base):
    __tablename__ = 'routes'

    id = sa.Column(sa.Integer, primary_key=True)
    point = sa.Column(sa.Integer, sa.ForeignKey('points.id'), nullable=False)
    meta = sa.Column(sa.Integer, sa.ForeignKey('routes_meta.id'), nullable=False)
    sequence = sa.Column(sa.Integer, server_default='0')


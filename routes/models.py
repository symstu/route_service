import typing
from collections import namedtuple

import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from config import conf

Base = declarative_base()
RouteMini = namedtuple('RouteMini', ['name', 'points'])
PointOut = namedtuple('PointOut', ['id', 'name', 'lat', 'lon'])


class Points(Base):
    __tablename__ = 'points'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    lat = sa.Column(sa.Float, nullable=False)
    lon = sa.Column(sa.Float, nullable=False)

    __table_args__ = (
        sa.Index('idx_points_id', 'id'),
    )

    @classmethod
    async def list(cls, offset: int, limit: int) -> typing.List[PointOut]:
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            *
        FROM points
        OFFSET $1
        LIMIT $2
        ''')
        return await request.fetch(offset, limit)


class RouteMeta(Base):
    __tablename__ = 'routes_meta'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

    __table_args__ = (
        sa.Index('idx_routes_meta_id_name', 'id', 'name'),
        sa.Index('idx_routes_meta_id', 'id'),
    )

    @classmethod
    async def list(cls, offset: int, limit: int):
        """
        Get list of created points

        :return: list of points
        """
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            rm.id as route_id, 
            min(rm.name) as route_name,
            array_agg(p.name) as points 
        FROM routes_meta rm
        JOIN routes r ON r.meta = rm.id
        JOIN points p ON r.point = p.id
        GROUP BY route_id
        OFFSET $1 
        LIMIT $2
        ''')
        data = await request.fetch(offset, limit)
        routes = dict()

        for point in data:
            route_name = point['route_name']
            routes[route_name] = {'id': point['route_id'],
                                  'points': point['points']}

        return routes

    @classmethod
    async def get(cls, name: str):
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
        WHERE r.name = $1
        ORDER BY r.id
        ''')
        return await request.fetch(name)

    @classmethod
    async def get_batch(cls, routes_ids: typing.List[int]):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            rm.id as meta_id, 
            rm.name as meta_name,
            p.name as point_name, 
            p.id as point_id, 
            p.lat as lat,
            p.lon as lon
        FROM routes_meta rm
        JOIN routes r ON r.meta = rm.id
        JOIN points p ON r.point = p.id
        WHERE rm.id = ANY($1::int[])
        ORDER BY r.id
        ''')
        return await request.fetch(routes_ids)

    @classmethod
    async def generate(cls, start: str, finish: str):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        SELECT 
            id, name
        FROM points
        WHERE 
            name = $1
        UNION ALL
        (SELECT 
            id, name
        FROM points
        WHERE 
            name <> $1 AND 
            name <> $2
        ORDER BY random()
        LIMIT 3)
        UNION ALL
        SELECT 
            id, name
        FROM points
        WHERE 
            name = $2
        ''')
        return await request.fetch(start, finish)

    @classmethod
    async def create(cls, name: str, points: typing.List[int]):
        conn = await conf.db_conn()
        request = await conn.prepare('''
        WITH new_meta AS (
            INSERT INTO routes_meta (name)
            VALUES ($1)
            RETURNING id
        )
        INSERT INTO routes (meta, point)
        SELECT 
            (SELECT id FROM new_meta), 
            arr
        FROM unnest($2::int[]) arr
        RETURNING meta
        ''')
        return await request.fetch(name, points)


class Routes(Base):
    __tablename__ = 'routes'

    id = sa.Column(sa.Integer, primary_key=True)
    point = sa.Column(sa.Integer, sa.ForeignKey('points.id'), nullable=False)
    meta = sa.Column(sa.Integer, sa.ForeignKey('routes_meta.id'), nullable=False)

    __table_args__ = (
        sa.Index('idx_routes_meta_field', 'meta'),
        sa.Index('idx_routes_meta_point', 'meta', 'point'),
    )

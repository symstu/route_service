import uuid

from hashlib import md5
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

    async def list(self, limit: int, offset: int):
        request = await conf.db_conn.prepare('''
        SELECT * FROM poins OFFSET $1 LIMIT $2
        ''')
        return await request.fetch(offset, limit)


class RouteMeta(Base):
    __tablename__ = 'routes_meta'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    @classmethod
    async def list(cls, limit: int, offset: int):
        """
        Get list of created points

        :param limit: limit per page
        :param offset: cursor
        :return: list of points
        """
        request = await conf.db_conn.prepare('''
        SELECT * FROM routes_meta OFFSET $1 LIMIT $2
        ''')
        return await request.fetch(offset, limit)

    @classmethod
    async def get(cls, start: int, finish: int):
        pass

    @classmethod
    async def create(cls, start: int, finish: int):
        pass


class Routes(Base):
    __tablename__ = 'routes'

    id = sa.Column(sa.Integer, primary_key=True)
    point = sa.Column(sa.Integer, sa.ForeingKey('points.id'), nullable=False)
    meta = sa.Column(sa.Integer, sa.ForeingKey('routes_meta.id'), nullable=False)
    sequence = sa.Column(sa.Integer, server_default='0')

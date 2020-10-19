import uuid

from hashlib import md5
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from config import conf

Base = declarative_base()


class UserRoute(Base):
    __tablename__ = 'users_routes'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    route_id = sa.Column(sa.Integer, nullabel=False)


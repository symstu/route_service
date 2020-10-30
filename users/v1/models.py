import uuid
import typing

from hashlib import md5

import sqlalchemy as sa

from asyncpg import exceptions

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config import conf
from v1 import exc


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    sessions = relationship('Session', cascade='all, delete')
    created_at = sa.Column(sa.DateTime, server_default='now()')

    __table_args__ = (sa.Index('idx_users_username_password',
                               'username', 'password'),)

    @staticmethod
    def gen_password(plain_password: str) -> str:
        return md5(plain_password.encode()).hexdigest()

    @classmethod
    async def authenticate(cls, token: str) -> dict:
        conn = await conf.db_conn()
        request = await conn.prepare('''
            SELECT
                u.id, u.username
            FROM
                users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.token = $1
        ''')
        result = await request.fetch(token)

        if not result:
            raise exc.InvalidToken

        user = result[0]
        return {'id': user.get('id'), 'username': user.get('username')}

    @classmethod
    async def authorize(cls, username: str, password: str) -> int:
        conn = await conf.db_conn()
        request = await conn.prepare('''
            SELECT id
            FROM users
            WHERE
                username = $1 AND
                password = $2
            LIMIT 1
        ''')
        return await request.fetchval(username, cls.gen_password(password))

    @classmethod
    async def login(cls, username: str, password: str) -> typing.Tuple[dict, str]:
        user_id = await cls.authorize(username, password)

        if not user_id:
            raise exc.UserNotFound

        return {'id': user_id, 'username': username}, await Session.create(user_id)

    @classmethod
    async def register(cls, username: str, password: str) -> typing.Tuple[dict, str]:
        conn = await conf.db_conn()
        request = await conn.prepare('''
            INSERT INTO users (username, password) VALUES 
            ($1, $2) RETURNING id;
        ''')

        try:
            user_id = await request.fetchval(username, cls.gen_password(password))
            return {'id': user_id, 'username': username}, await Session.create(user_id)

        except exceptions.UniqueViolationError:
            raise exc.UserAlreadyExists

    @classmethod
    async def logout(cls, user_id: int):
        return await Session.remove(user_id)

    @classmethod
    async def remove(cls, user_id: int):
        conn = await conf.db_conn()
        request = await conn.prepare('select delete_user($1)')
        return request.fetchval(user_id)


class Session(Base):
    __tablename__ = 'sessions'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    token = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), unique=True)
    created_at = sa.Column(sa.DateTime, primary_key=True, server_default='now()')

    __table_args__ = (sa.Index('idx_sessions_token', 'token'),)

    @classmethod
    async def create(cls, user_id: int):
        conn = await conf.db_conn()
        request = await conn.prepare('''
            INSERT INTO sessions (user_id, token) VALUES ($1, $2)
            ON CONFLICT (user_id) DO 
                UPDATE SET token = EXCLUDED.token WHERE sessions.user_id = $1
            RETURNING id
        ''')
        session = str(uuid.uuid4())
        await request.fetchval(user_id, session)
        return session

    @classmethod
    async def remove(cls, user_id: int):
        conn = await conf.db_conn()
        request = await conn.prepare('''
            DELETE FROM sessions WHERE user_id = $1 RETURNING id
        ''')
        return await request.fetchval(user_id)

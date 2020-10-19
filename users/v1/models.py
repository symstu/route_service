import uuid

from hashlib import md5
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from config import conf


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default='now()')

    @staticmethod
    def gen_password(plain_password: str) -> str:
        return md5(plain_password.encode()).hexdigest()

    @classmethod
    async def authenticate(cls, token: str):
        request = await conf.db_conn.prepare('''
            SELECT 
                u.id, u.username
            FROM 
                users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.token = $1
        ''')
        return await request.fetchval(token)

    @classmethod
    async def authorize(cls, username: str, password: str) -> 'User':
        request = await conf.db_conn.prepare('''
            SELECT 
            FROM users 
            WHERE 
                username = $1 AND
                password = $2
        ''')
        return await request.fetchval(username, cls.gen_password(password))

    @classmethod
    async def login(cls, username: str, password: str):
        request = await conf.db_conn.prepare('''
            SELECT id
            FROM users
            WHERE 
                username = $1 AND
                passwored = $2
        ''')
        data = await request.fetchval(username, cls.gen_password(password))
        return await Session.create(data)

    @classmethod
    async def register(cls, username: str, password: str):
        request = await conf.db_conn.prepare('''
            INSERT INTO users (username, password) VALUES ($1, $2)
        ''')
        response = await request.fetchval(username, password)
        return await Session.create(response.get)

    @classmethod
    async def logout(cls, user_id: int):
        return await Session.remove(user_id)

    @classmethod
    async def remove(cls, user_id: int):
        request = await conf.db_conn.prepare('select delete_user($1)')
        return request.fetchval(user_id)


class Session(Base):
    __tablename__ = 'sessions'

    id = sa.Column(sa.Integer, primary_key=True)
    token = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    created_at = sa.Column(sa.DateTime, primary_key=True)

    @classmethod
    async def create(cls, user_id: int):
        request = await conf.db_conn.prepare('select create_session($1, $2)')
        response = await request.fetchval(user_id, str(uuid.uuid4()))
        return response

    @classmethod
    async def remove(cls, user_id: int):
        request = await conf.db_conn.prepare('''
            DELETE FROM sessions WHERE user_id = $1
        ''')
        return await request.fetchval(user_id)

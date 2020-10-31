import os
import asyncpg


class TestConfig:
    db_host: str = os.environ.get('db_host', 'localhost')
    db_port: int = os.environ.get('db_port', 5432)
    db_user: str = os.environ.get('db_user', 'postgres')
    db_password: str = os.environ.get('db_password', 'postgres')
    db_name: str = os.environ.get('db_name', 'web_routes')

    __db_conn: asyncpg.Connection = None

    @property
    def db_url(self):
        return f'postgresql://{self.db_user}:{self.db_password}@' \
               f'{self.db_host}:{self.db_port}/{self.db_name}'

    async def db_conn(self) -> asyncpg.Connection:
        if self.__db_conn is None:
            self.__db_conn = await asyncpg.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
            )

        return self.__db_conn


conf = TestConfig()
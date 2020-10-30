import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command, config as alembic_config
from config import conf, TestConfig


def create_test_db(config: TestConfig):
    original_db_name = config.db_name
    config.db_name = 'postgres'
    new_engine = create_engine(config.db_url)

    session = sessionmaker(bind=new_engine)()
    session.connection().connection.set_isolation_level(0)
    session.execute(f'drop database if exists {original_db_name}')
    session.execute(f'create database {original_db_name}')
    session.close()

    config.db_name = original_db_name
    conf = alembic_config.Config('alembic.ini')
    conf.set_section_option(
        'alembic', 'sqlalchemy.url', config.db_url)
    print(f' Upgrading database {config.db_url}')
    command.upgrade(conf, 'head')


@pytest.fixture(scope='session', autouse=True)
def create_database():
    create_test_db(conf)

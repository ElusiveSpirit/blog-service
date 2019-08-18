import os

import pytest
from asyncpg.transaction import Transaction

from app.app import create_app
from app.utils.db import create_db_pool
from tests.utils import get_postgres_docker_container, get_redis_docker_container


@pytest.fixture(scope='session')
def prepare_settings():
    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.test')


@pytest.fixture(scope='session')
def postgres_service(prepare_settings, docker, session_id, unused_port):
    container = get_postgres_docker_container(docker.containers, session_id, unused_port())

    try:
        yield container
    finally:
        container.kill()
        container.remove()


@pytest.fixture(scope='session')
def cache_service(prepare_settings, docker, session_id, unused_port):
    container = get_redis_docker_container(docker.containers, session_id, unused_port())
    try:
        yield container
    finally:
        container.kill()
        container.remove()


@pytest.fixture(scope='function')
async def transact_conn(postgres_service):
    db_pool = await create_db_pool()
    async with db_pool.acquire() as connection:
        # Open a transaction.
        tr: Transaction = connection.transaction()
        await tr.start()
        try:
            yield connection
        except Exception as e:
            await tr.rollback()
            raise e


@pytest.fixture()
def cli(loop, aiohttp_client, transact_conn, cache_service):
    app = loop.run_until_complete(create_app())
    app.conn = transact_conn
    return loop.run_until_complete(aiohttp_client(app))

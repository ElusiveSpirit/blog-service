import logging

import asyncpg
import pytest

from app.app import create_app
from app.utils.db import create_db_pool

logging.disable(logging.CRITICAL)


@pytest.fixture(scope='function')
async def db_pool(loop):
    return await create_db_pool()


@pytest.fixture(scope='function')
async def transact(db_pool: asyncpg.pool.Pool):
    async with db_pool.acquire() as connection:
        # Open a transaction.
        tr: asyncpg.connection.transaction.Transaction = connection.transaction()
        await tr.start()
        try:
            yield connection
        except Exception as e:
            await tr.rollback()
            raise e


@pytest.fixture()
def cli(loop, aiohttp_client, transact):
    app = loop.run_until_complete(create_app())
    app.conn = transact
    return loop.run_until_complete(aiohttp_client(app))

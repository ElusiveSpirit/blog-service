import pytest
import uvloop
from asyncpg import Connection

from app.utils.models import ModelManager


@pytest.fixture()
async def test_manager(loop: uvloop, transact_conn: Connection):
    await transact_conn.execute("""
        CREATE TABLE test_table (
          id SERIAL PRIMARY KEY,
          name VARCHAR(255)
        )
    """)

    class TestManager(ModelManager):

        class Meta:
            db_table = 'test_table'

    yield TestManager(transact_conn)


async def test_insert_value(test_manager: ModelManager, transact_conn: Connection):
    await test_manager.insert_value(name='name1')

    rows = await transact_conn.fetch("SELECT * FROM test_table")

    assert rows == [(1, 'name1')]


async def test_fetch_zero_rows(test_manager: ModelManager):
    assert await test_manager.fetch_all() == []


async def test_fetch_one_row(test_manager: ModelManager):
    await test_manager.insert_value(name='name1')
    assert await test_manager.fetch_all() == [(1, 'name1')]


async def test_fetch_multiple_rows(test_manager: ModelManager):
    await test_manager.insert_value(name='name1')
    await test_manager.insert_value(name='name2')
    assert await test_manager.fetch_all() == [(1, 'name1'), (2, 'name2')]


async def test_fetch_row_by_id(test_manager: ModelManager):
    await test_manager.insert_value(name='name1')
    await test_manager.insert_value(name='name2')
    assert await test_manager.fetch_by('id', 1) == (1, 'name1')
    assert await test_manager.fetch_by('id', 2) == (2, 'name2')


async def test_fetch_row_by_name(test_manager: ModelManager):
    await test_manager.insert_value(name='name1')
    await test_manager.insert_value(name='name2')
    await test_manager.insert_value(name='name2')
    assert await test_manager.fetch_by('name', 'name1') == (1, 'name1')
    assert await test_manager.fetch_by('name', 'name2') == (2, 'name2')
    assert await test_manager.fetch_by('name', 'name2', limit=100) == [(2, 'name2'), (3, 'name2')]

from asyncpg import Connection, connect
from asyncpg.pool import Pool, create_pool

from app.utils import settings


async def get_raw_connection() -> Connection:
    return await connect(
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
    )


async def create_database(db_name: str, conn: Connection = None) -> None:
    if conn is None:
        conn = await get_raw_connection()
    await conn.execute(f'CREATE DATABASE {db_name}')


async def drop_database(db_name: str, conn: Connection = None) -> None:
    if conn is None:
        conn = await get_raw_connection()
    await conn.execute(f'DROP DATABASE IF EXISTS {db_name}')


async def create_db_pool() -> Pool:
    """PgSQL creating connection pool
    Application settings. Sets db_pool attr after initializing

    :return: asyncpg pool connection
    """
    pool: Pool = await create_pool(
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
    )
    settings.db_pool = pool

    return pool


async def get_db_connection() -> Connection:
    """PgSQL connection function
    """
    if not settings.db_pool:
        await create_db_pool()
    async with settings.db_pool.acquire() as conn:
        return conn

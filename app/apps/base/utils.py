from typing import Dict

import asyncpg

from app.utils import settings


async def get_db_health_status() -> str:
    try:
        async with settings.db_pool.acquire() as conn:
            await conn.execute('SELECT 123')
            return 'ok'
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        return 'no connection'


async def get_health_status() -> Dict[str, str]:
    health = {
        'db': await get_db_health_status()
    }
    return health

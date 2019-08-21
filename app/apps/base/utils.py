import logging
from typing import Dict

import asyncpg
from aiohttp.web_request import Request
from aioredis import Redis, RedisError

logger = logging.getLogger(__name__)


async def get_redis_health_status(request: Request) -> str:
    try:
        _: Redis = request.redis
        return 'ok'
    except (RedisError, AttributeError):
        return 'no connection'
    except Exception as e:
        logger.error('Redis health error', exc_info=e)
        return 'error'


async def get_db_health_status(request: Request) -> str:
    try:
        await request.conn.execute('SELECT 123')
        return 'ok'
    except (asyncpg.exceptions.ConnectionDoesNotExistError, AttributeError):
        return 'no connection'
    except Exception as e:
        logger.error('DB health error', exc_info=e)
        return 'error'


async def get_health_status(request: Request) -> Dict[str, str]:
    health = {
        'db': await get_db_health_status(request),
        'redis': await get_redis_health_status(request),
    }
    return health

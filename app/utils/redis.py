from aioredis import create_redis, Redis

from app.utils import settings


async def get_redis() -> Redis:
    """Return high-level redis interface connection
    """
    return await create_redis(
        address=settings.REDIS_ADDRESS,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
    )

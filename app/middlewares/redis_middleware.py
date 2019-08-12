from typing import Callable

from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from app.utils.redis import get_redis


@middleware
async def redis_middleware(request: Request, handler: Callable) -> Response:
    request.redis = await get_redis()
    try:
        return await handler(request)
    except Exception:
        request.redis.close()
        await request.redis.wait_closed()
        raise

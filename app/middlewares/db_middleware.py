from typing import Callable

from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from app.utils import settings


@middleware
async def db_middleware(request: Request, handler: Callable) -> Response:
    async with settings.db_pool.acquire() as conn:
        app_conn = getattr(request.app, 'conn', None)
        if app_conn:
            # Use single conn from app for test cases to rollback all sub transactions
            request.conn = app_conn
        else:
            request.conn = conn
        return await handler(request)

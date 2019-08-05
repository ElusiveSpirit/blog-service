from aiohttp.web_middlewares import middleware

from app.utils import settings


@middleware
async def db_middleware(request, handler):
    async with settings.db_pool.acquire() as conn:
        if getattr(request.app, 'conn', None):
            # Use single conn from app for test cases to rollback all sub transactions
            request.conn = request.app.conn
        else:
            request.conn = conn
        return await handler(request)

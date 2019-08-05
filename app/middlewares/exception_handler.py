from aiohttp.web_middlewares import middleware

from app.utils.web_exceptions import HTTPException


@middleware
async def exception_handler(request, handler):
    try:
        return await handler(request)
    except HTTPException as e:
        return e

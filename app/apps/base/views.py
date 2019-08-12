from typing import Dict

from aiohttp.web_request import Request
from aiohttp.web_response import Response

from app.apps.base.utils import get_health_status
from app.utils.web_response import json_response


async def health_handler(request: Request) -> Response:
    """Indicates app health
    """
    health: Dict = await get_health_status(request)
    is_ok: bool = all(v == 'ok' for v in health.values())
    return json_response(health, status=200 if is_ok else 400)


async def index_handler(request: Request) -> Response:
    return json_response({'app': 'aiohttp-template'}, status=200)

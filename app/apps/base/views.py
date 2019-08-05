from typing import Dict

from app.apps.base.utils import get_health_status
from app.utils.web_response import json_response


async def health_handler(request):
    """Indicates app health
    """
    health: Dict = await get_health_status()
    is_ok: bool = all(v == 'ok' for v in health.values())
    return json_response(health, status=200 if is_ok else 400)


async def index_handler(request):
    return json_response({'app': 'aiohttp-template'}, status=200)

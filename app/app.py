import logging
import logging.config
import os

from aiohttp.web import Application
from asyncpg.pool import Pool

from app.middlewares import db_middleware, exception_handler, redis_middleware
from app.utils import LazySettings
from app.utils.db import create_db_pool

logger = logging.getLogger(__name__)


async def create_app() -> Application:
    """Fabric creating web app"""
    from app.utils import settings

    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.dev')

    app = Application()
    await initialize_config(app, settings)
    await initialize_db(app)

    await initialize_routes(app)
    await initialize_plugins(app)
    await initialize_middlewares(app)

    return app


async def initialize_config(app: Application, settings: LazySettings) -> None:
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    app['config'] = settings


async def initialize_db(app: Application) -> None:
    db_pool = await create_db_pool()

    app['db_pool'] = db_pool

    app.on_cleanup.append(close_db)


async def close_db(app: Application) -> None:
    db_pool: Pool = app['db_pool']
    await db_pool.close()


async def initialize_routes(app: Application) -> None:
    from config.routes import routes
    api_prefix = app['config'].API_PREFIX

    for route in routes:
        app.router.add_route(route[0], api_prefix + route[1], route[2], name=route[3])


async def initialize_plugins(app: Application) -> None:
    pass


async def initialize_middlewares(app: Application) -> None:
    from app.apps.auth.middlewares import jwt_middleware

    app.middlewares.extend([
        exception_handler,
        db_middleware,
        redis_middleware,
        jwt_middleware,
    ])

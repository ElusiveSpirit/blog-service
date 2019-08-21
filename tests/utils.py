import asyncio

import asyncpg
from docker.models.containers import Container, ContainerCollection

from app.utils import settings
from app.utils.db import apply_migrations, create_db_pool


async def migrate() -> bool:
    timeout = 0.001
    for i in range(100):
        try:
            pool = await create_db_pool()
        except (asyncpg.PostgresError, OSError):
            await asyncio.sleep(timeout)
            timeout *= 2
        else:
            async with pool.acquire() as conn:
                await apply_migrations(conn)
            await pool.close()
            return True
    else:
        return False


def migrate_pg() -> None:
    import asyncio

    has_connection = asyncio.run(migrate())

    if not has_connection:
        raise RuntimeError('Cannot connect to postgres server.')


def get_postgres_docker_container(containers: ContainerCollection, session_id: str, unused_port: int) -> Container:
    settings.POSTGRES_PORT = unused_port
    container = containers.run(
        'postgres:11-alpine',
        name=f'postgres-aiohttp-{session_id}',
        environment={
            'POSTGRES_USER': settings.POSTGRES_USER,
            'POSTGRES_PASSWORD': settings.POSTGRES_PASSWORD,
            'POSTGRES_DB': settings.POSTGRES_DB,
        },
        ports={'5432': settings.POSTGRES_PORT},
        detach=True)
    migrate_pg()
    return container


def get_redis_docker_container(containers: ContainerCollection, session_id: str, unused_port: int) -> Container:
    settings.REDIS_ADDRESS = f'redis://localhost:{unused_port}'
    container = containers.run('redis', name=f'redis-aiohttp-{session_id}', ports={'6379': unused_port}, detach=True)
    return container

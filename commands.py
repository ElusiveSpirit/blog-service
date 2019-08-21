#!/usr/bin/env python
import asyncio
import logging
import os
import sys
import traceback
from functools import wraps
from subprocess import call

import click
import uvloop
from aiohttp_devtools.cli import app_factory_help, aux_port_help, debugtoolbar_help, host_help, port_help, verbose_help
from aiohttp_devtools.exceptions import AiohttpDevException
from aiohttp_devtools.logs import main_logger, setup_logging
from aiohttp_devtools.runserver import INFER_HOST, run_app
from aiohttp_devtools.runserver import runserver as _runserver
from asyncpg import InvalidCatalogNameError

from app.utils import settings
from app.utils.db import create_database, drop_database

logger = logging.getLogger(__name__)

_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=False)
_file_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=True)
_dir_may_exist = click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True)

uvloop.install()


def setup():
    """
    Set up the application:
        - configure settings
        - connect db
    """
    from app.utils.db import create_db_pool

    # settings.configure()
    try:
        asyncio.run(create_db_pool())
    except InvalidCatalogNameError:
        logger.warning(f'⚠️  Database {settings.POSTGRES_DB} doesn\'t exists')


def setup_app_env(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        setup()
        return func(*args, **kwargs)

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.argument('app-path', envvar='AIO_APP_PATH', type=_file_dir_existing, default='app')
@click.option('--host', default=INFER_HOST, help=host_help)
@click.option('--debug-toolbar/--no-debug-toolbar', envvar='AIO_DEBUG_TOOLBAR', default=None, help=debugtoolbar_help)
@click.option('--app-factory', 'app_factory_name', envvar='AIO_APP_FACTORY', help=app_factory_help)
@click.option('-p', '--port', 'main_port', envvar='AIO_PORT', type=click.INT, help=port_help)
@click.option('--aux-port', envvar='AIO_AUX_PORT', type=click.INT, help=aux_port_help)
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
def runserver(**config):
    """
    Run a development server for an aiohttp apps.
    Takes one argument "app-path" which should be a path to either a directory containing a recognized default file
    ("app.py" or "main.py") or to a specific file. Defaults to the environment variable "AIO_APP_PATH" or ".".
    The app path is run directly, see the "--app-factory" option for details on how an app is loaded from a python
    module.
    """
    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.dev')

    active_config = {k: v for k, v in config.items() if v is not None}
    setup_logging(config['verbose'])
    try:
        run_app(*_runserver(**active_config))
    except AiohttpDevException as e:
        if config['verbose']:
            tb = click.style(traceback.format_exc().strip('\n'), fg='white', dim=True)
            main_logger.warning('AiohttpDevException traceback:\n%s', tb)
        main_logger.error('Error: %s', e)
        sys.exit(2)


@cli.command()
@click.argument('collection')
def clear_database(collection):
    click.echo(f'Dropping collection {collection}...')
    asyncio.run(drop_database(settings.POSTGRES_DB))
    asyncio.run(create_database(settings.POSTGRES_DB))


@cli.command()
@click.option('--settings', 'settings_module', default='config.settings.test')
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
@click.option('-c', '--coverage', help='With coverage')
@click.pass_context
def test(ctx, settings_module, **config):
    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', settings_module)
    if settings.DATABASE_CLEAR:
        ctx.invoke(clear_database, collection=settings.POSTGRES_DB)
    setup()
    call_stack = ['py.test']
    if config['coverage']:
        call_stack.append(f'--cov={config["coverage"]}')
    call(call_stack)


@cli.command()
@click.option('--ipython', default=True)
def shell(ipython):
    os.environ.setdefault('AIOHTTP_SETTINGS_MODULE', 'config.settings.dev')
    setup()

    def run_ipython():
        from IPython import start_ipython
        start_ipython(argv=[])

    def run_python():
        import code

        imported_objects = {'settings': settings}

        code.interact(local=imported_objects)

    if ipython is True or ipython == 'True':
        run_ipython()
    else:
        run_python()


if __name__ == '__main__':
    cli()

"""wsgi.py entry point"""
import asyncio

import uvloop
from aiohttp.web import run_app

from app.app import create_app

uvloop.install()

awaitable_app = create_app()

if __name__ == '__main__':
    run_app(awaitable_app)

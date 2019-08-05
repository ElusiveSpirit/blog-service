"""wsgi.py entry point"""
import asyncio

from aiohttp.web import run_app

from app.app import create_app

app = asyncio.run(create_app())

if __name__ == '__main__':
    run_app(app)

from .base import *

DEBUG = True

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'aiohttp')

REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'redis://redis')

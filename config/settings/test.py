from .base import *

# CORE
####################

DEBUG = False

SECRET_KEY = 'kj3h12iu3yhl12ih3;o'

# DATABASE
####################
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = 'aiohttp_test'
DATABASE_CLEAR = True

REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'redis://redis')

API_PREFIX = ''

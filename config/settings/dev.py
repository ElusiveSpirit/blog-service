import os

# CORE
####################

DEBUG = True

SECRET_KEY = 'kj3h12iu3yhl12ih3;o'

# DATABASE
####################
POSTGRES_HOST = os.getenv('POSTGRES_HOST', default='localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', default='postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', default='aiohttp')

API_PREFIX = ''

"""
Default AioHTTP settings. Override these with settings in the module pointed to
by the AIOHTTP_SETTINGS_MODULE environment variable.
"""

####################
# CORE             #
####################

DEBUG = False

INSTALLED_APPS = []

POSTGRES_HOST = None
POSTGRES_USER = None
POSTGRES_PASSWORD = None
POSTGRES_DB = None
POSTGRES_PORT = 5432

REDIS_ADDRESS = None
REDIS_DB = 0
REDIS_PASSWORD = None

SECRET_KEY = ''

# JWT settings
JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = 'HS256'

TIME_ZONE = 'UTC'

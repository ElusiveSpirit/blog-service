"""
Default AioHTTP settings. Override these with settings in the module pointed to
by the AIOHTTP_SETTINGS_MODULE environment variable.
"""

####################
# CORE             #
####################

DEBUG = False

INSTALLED_APPS = []

DATABASE_HOST = None
DATABASE_USER = None
DATABASE_PASSWORD = None
DATABASE_NAME = None

SECRET_KEY = ''

# JWT settings
JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = 'HS256'

TIME_ZONE = 'UTC'

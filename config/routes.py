"""Application roots
"""
from app.apps.base.views import health_handler, index_handler

routes = [
    ('*', '/', index_handler, 'index'),
    ('*', '/health/', health_handler, 'health'),
]

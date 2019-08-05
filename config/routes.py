"""Application roots
"""
from app.apps.base.views import index_handler, health_handler

routes = [
    ('*', '/', index_handler, 'index'),
    ('*', '/health/', health_handler, 'health'),
]

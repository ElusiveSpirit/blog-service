"""
Global exception and warning classes.
"""


class ImproperlyConfigured(Exception):
    """App is somehow improperly configured"""
    pass


class ManagerTableDoesNotSpecified(Exception):
    """Manager table does not specified in Meta subclass"""
    pass

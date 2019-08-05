from app.utils.web_exceptions import HTTPUnauthorized


def _check_for_user(request):
    if not request.user:
        raise HTTPUnauthorized()


def login_required(func):
    async def wrapper(request):
        _check_for_user(request)
        return await func(request)
    return wrapper

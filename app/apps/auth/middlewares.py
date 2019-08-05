import jwt
from aiohttp.web_middlewares import middleware

from app.utils import settings
from app.utils.web_exceptions import HTTPBadRequest


@middleware
async def jwt_middleware(request, handler):
    request.user = None
    jwt_token = request.headers.get('authorization', None)
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET,
                                 algorithms=[settings.JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise HTTPBadRequest('Token is invalid')

        # request.user = User.get(payload['user_id'])
    return await handler(request)

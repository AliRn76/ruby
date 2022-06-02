from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from user.authentication import JWTAuthentication


@database_sync_to_async
def get_user(token_key: str) -> any:
    user, _  = JWTAuthentication.authenticate_credentials(token_key)
    return user


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split('&')))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = None if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)

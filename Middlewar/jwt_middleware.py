import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.db import close_old_connections
from django.contrib.auth import get_user_model

from utils.jwt import JWTManager
User = get_user_model()
from urllib.parse import parse_qs

class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Bearer':
                try:
                    decoded_data = JWTManager.decode_token(token_key)
                    user_id = decoded_data['id']
                    user_email = decoded_data['email']
                    user = await self.get_token(user_id, user_email)
                    if not user:
                        raise Exception('Invalid token')
                    scope['user'] = user
                except Exception as e:
                    scope['user'] = AnonymousUser()
                    await send({
                        "type": "websocket.close",
                        "code": 1000,
                    })
                    return
        result = await self.inner(scope, receive, send)
        return result

    @database_sync_to_async
    def get_token(self, user_id, user_email):
        try:
            user = User.objects.get(id=user_id, email=user_email)
            return user
        except User.DoesNotExist:
            return None

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .settings import *

from apps.room.sockets import websocket_urlpatterns
from channels.layers import get_channel_layer

django_asgi_app = get_asgi_application()

from Middlewar.jwt_middleware import JwtAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Obtén el objeto ChannelLayer
channel_layer = get_channel_layer()

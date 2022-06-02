from django.urls import path
from websocket.consumers import RubyConsumer
from websocket.middlewares import JWTAuthMiddleware
from channels.security.websocket import OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        JWTAuthMiddleware(
            URLRouter([
                path('ws/', RubyConsumer.as_asgi()),
            ])
        ),
        ['*'],
    ),
})

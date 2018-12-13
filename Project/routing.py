from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from core.consumers import *

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("chat/stream/", ChatConsumer),
            path("notify/", NoseyConsumer),
            path("message/", MessageConsumer),
        ]),
    ),
})
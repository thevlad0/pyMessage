"""
ASGI config for pyMessage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from messaging.consumers import ChatConsumer, OnlineStatusConsumer, NotificationConsumer
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyMessage.settings')
application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', ChatConsumer),
            path('ws/online/', OnlineStatusConsumer),
            path('ws/notify/', NotificationConsumer)
        ])
    )
})

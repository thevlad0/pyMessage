from django.urls import path
from .consumers import ChatConsumer, OnlineStatusConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
    path('ws/online/', OnlineStatusConsumer.as_asgi()),
    path('ws/notify/', NotificationConsumer.as_asgi())
]
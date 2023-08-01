from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('wss/', ChatConsumer.as_asgi()),  # Using ASGI
]
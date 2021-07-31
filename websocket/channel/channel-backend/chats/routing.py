from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chats/<slug:pub_id>/', ChatConsumer),
]

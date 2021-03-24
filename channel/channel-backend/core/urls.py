from django.urls import path

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('chat/add/', add_chat, name='add_chat'),
    path('chat/<slug:pub_id>/', chat_room, name='chat_room'),
]

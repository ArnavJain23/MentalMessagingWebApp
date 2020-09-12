from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/chat/<path:room_name>/", consumers.ChatConsumer),
]

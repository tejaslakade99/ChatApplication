from django.urls import path
from .consumers import *

websocket_urlpatterns = [
  path("wss/groupchat/<groupchat_name>/", GroupChatConsumer.as_asgi()),
]
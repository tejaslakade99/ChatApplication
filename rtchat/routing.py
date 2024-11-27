from django.urls import path
from .consumers import *

websocket_urlpatterns = [
  path("ws/groupchat/<groupchat_name>/", GroupChatConsumer.as_asgi()),
]
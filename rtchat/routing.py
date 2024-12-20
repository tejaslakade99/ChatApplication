from django.urls import re_path
from .consumers import GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/groupchat/(?P<groupchat_name>\w+)/$', GroupChatConsumer.as_asgi()),
]

from django.urls import path
from . import views

urlpatterns = [
  path("",views.index, name="index"),
  path("chat/<username>/", views.get_or_create_chatroom, name="start-chat"),
  path("chat/room/<group_name>", views.index, name="chatroom"),
]
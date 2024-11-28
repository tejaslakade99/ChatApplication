from django.urls import path
from . import views

urlpatterns = [
  path("",views.index, name="index"),
  path("chat/<username>/", views.get_or_create_chatroom, name="start-chat"),
  path("chat/room/<group_name>/", views.index, name="chatroom"),
  path("chat/group/<group_name>/",views.create_group_chat, name="new-groupchat"),
  path("chat/group/add/<groupname>/", views.add_in_group, name="add-in-group"),
  path("chat/group/remove/<groupname>/", views.remove_in_group, name="remove-in-group"),
]
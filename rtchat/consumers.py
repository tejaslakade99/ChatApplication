from channels.generic.websocket import WebsocketConsumer
from .services.message_service import MessageService
from .services.presence_service import PresenceService
from .services.template_render_service import TemplateRenderService
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from .models import *
import json

# This class handles the WebSocket connection for group chat.
# It allows users to connect, disconnect, and send messages in a group chat.
class GroupChatConsumer(WebsocketConsumer):
  connected_users = {}

  def connect(self):
    self.user = self.scope['user']
    print("Connecting user:", self.user, "| Authenticated:", self.user.is_authenticated)
    self.groupchat_name = self.scope['url_route']['kwargs']['groupchat_name']
    self.groupchat = get_object_or_404(GroupChat, group_name=self.groupchat_name)
    
    async_to_sync(self.channel_layer.group_add)(
      self.groupchat_name, self.channel_name
    )
    
    user_key = f"{self.groupchat.pk}-{self.user.pk}"
    if user_key not in self.connected_users:
      self.connected_users[user_key] = 0
    self.connected_users[user_key] += 1
    
    if self.connected_users[user_key] == 1:
      if isinstance(self.user, type(self.groupchat.members.first())):
        PresenceService.add_user(self.groupchat, self.user)
        self.send_online_users_update()

    self.accept()

  def disconnect(self, code):    
    async_to_sync(self.channel_layer.group_discard)(
      self.groupchat_name, self.channel_name
    )
    
    user_key = f"{self.groupchat.pk}-{self.user.pk}"
    self.connected_users[user_key] -= 1
    
    if self.connected_users[user_key] == 0:
      PresenceService.remove_user(self.groupchat, self.user)
      self.send_online_users_update()
    
    print(f"WebSocket disconnected with close code: {code}")
  
  def receive(self, text_data=None):
    try:
      data = json.loads(text_data)
      chat = MessageService.create_message(data['body'], self.user, self.groupchat)
      
      async_to_sync(self.channel_layer.group_send)(
        self.groupchat_name,
        {
          'type': 'chat_handler',
          'chat_id': chat.id,
        }
      )
    except Exception as e:
      print(f"Error receiving message: {e}")
      self.close()
      
  def chat_handler(self, event):
    chat_id = event['chat_id']
    chat = GroupMessages.objects.get(id=chat_id)
    
    html = TemplateRenderService.render_chat_message(chat, self.user)
    self.send(text_data=html)
  
  def online_users_handler(self, event):
    try:
      online_users = event['online_users']
      html = TemplateRenderService.render_online_users(online_users)
      self.send(text_data=html)
    except Exception as e:
      print("Error Occured",e)
      
  def send_online_users_update(self):
    online_users = PresenceService.update_online_users(self.groupchat)
    async_to_sync(self.channel_layer.group_send)(self.groupchat_name, {
        'type': 'online_users_handler',
        'online_users': online_users
    })
  
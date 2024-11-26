from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import *
import json

class GroupChatConsumer(WebsocketConsumer):
  
  def connect(self):
    self.user = self.scope['user']
    self.groupchat_name = self.scope['url_route']['kwargs']['groupchat_name']
    self.groupchat = get_object_or_404(GroupChat, group_name=self.groupchat_name)
    
    async_to_sync(self.channel_layer.group_add)(
      self.groupchat_name, self.channel_name
    )
    self.accept()
    
  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.groupchat_name, self.channel_name
    )
    
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    body = text_data_json['body']
    
    chat = GroupMessages.objects.create(
      body = body,
      author = self.user,
      group = self.groupchat
    )
  
    event = {
      'type': 'chat_handler',
      'chat_id':chat.id,
    }
    
    async_to_sync(self.channel_layer.group_send)(
      self.groupchat_name, event
    )
    
  def chat_handler(self, event):
    chat_id = event['chat_id']
    chat = GroupMessages.objects.get(id= chat_id)
    context = {
      'chat':chat,
      'user':self.user,
    }
    
    html = render_to_string('partials/chat_message_p.html', context=context)
    self.send(text_data=html)
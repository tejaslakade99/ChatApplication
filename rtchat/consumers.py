from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import *
import json

class GroupChatConsumer(WebsocketConsumer):
  
  def connect(self):
    self.user = self.scope['user']
    self.groupchat_name = self.scope['url_route']['kwargs']['groupchat_name']
    self.groupchat = get_object_or_404(GroupChat, group_name=self.groupchat_name)
    self.accept()
    
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    body = text_data_json['body']
    
    chat = GroupMessages.objects.create(
      body = body,
      author = self.user,
      group = self.groupchat
    )
    
    context = {
      'chat':chat,
      'user':self.user,
    }
    
    html = render_to_string('partials/chat_message_p.html', context=context)
    self.send(text_data=html)
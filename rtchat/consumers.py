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

    # add and update online users
    if self.user not in self.groupchat.users_online.all():
      self.groupchat.users_online.add(self.user)
      self.groupchat.save() 
      self.update_online_users()
    
    print("Online users after connect:", self.groupchat.users_online.all())
    self.accept()
    
  def disconnect(self,code):
    async_to_sync(self.channel_layer.group_discard)(
      self.groupchat_name, self.channel_name
    )
    print(f"WebSocket disconnected with close code: {code}")
    # remove and update online users
    if self.user in self.groupchat.users_online.all():
      self.groupchat.users_online.remove(self.user)
      self.groupchat.save()
      self.update_online_users()
    print("Online users after disconnect:", self.groupchat.users_online.all())
    
  def receive(self, text_data):
    try:
      text_data_json = json.loads(text_data)
      body = text_data_json['body']

      self.groupchat.refresh_from_db()
  
      chat = GroupMessages.objects.create(
          body=body,
          author=self.user,
          group=self.groupchat
      )
  
      event = {
          'type': 'chat_handler',
          'chat_id': chat.id,
      }
      async_to_sync(self.channel_layer.group_send)(
          self.groupchat_name, event
      )
    
      self.update_online_users()
    
    except Exception as e:
      print(f"Error receiving message: {e}")
      self.close()
    
  def chat_handler(self, event):
    chat_id = event['chat_id']
    chat = GroupMessages.objects.get(id= chat_id)

    context = {
      'chat':chat,
      'user':self.user,
    }
    
    html = render_to_string('partials/chat_message_p.html', context=context)
    self.send(text_data=html)
    
  def update_online_users(self):
    allUsers = User.objects.all()
    online_users = self.groupchat.users_online.all()
    members = self.groupchat.members.all() or allUsers
    online_users_with_avatars = []
    for user in members:
      if user in online_users:
        profile = Profile.objects.get(user=user)
        online_users_with_avatars.append({
          'username':user.username,
          'avatar':profile.avatar,
          'status':'online'
        })
      else:
        profile = Profile.objects.get(user=user)
        online_users_with_avatars.append({
          'username':user.username,
          'avatar':profile.avatar,
          'status':'offline'
        })
        
    
    event = {
        'type': 'online_users_handler',
        'online_users': online_users_with_avatars,
    }
    
    async_to_sync(self.channel_layer.group_send)(self.groupchat_name, event)
    
  def online_users_handler(self, event):
    try:  
      online_users = event['online_users']
      html = render_to_string('partials/online_users_p.html', {'online_users':online_users})
      self.send(text_data=html)
    except Exception as e:
      print(e)
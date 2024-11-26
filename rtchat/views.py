from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request):
  avatar = get_object_or_404(Profile, user__username=request.user.username)
  groupChat = get_object_or_404(GroupChat, group_name='Friends')
  chats = GroupMessages.objects.filter(group=groupChat)
  form = ChatMessageCreateForm(request.POST)
  
  if request.htmx:
    form = ChatMessageCreateForm(request.POST)
    if form.is_valid():
      chat = form.save(commit=False)
      chat.author = request.user
      chat.group = groupChat
      chat.save()
      context = {
        'chat':chat,
        'user':request.user,
      }
      return render(request, 'partials/chat_message_p.html', context)
      
  return render(request, 'rtchat/index.html', {'avatar':avatar, 'chats':chats, 'form':form})
    
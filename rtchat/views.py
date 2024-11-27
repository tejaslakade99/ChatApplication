from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request, group_name='Friends'):
  avatar = get_object_or_404(Profile, user__username=request.user.username)
  groupChat = get_object_or_404(GroupChat, group_name=group_name)
  chats = GroupMessages.objects.filter(group=groupChat)
  form = ChatMessageCreateForm(request.POST)
  allPrivateChats = GroupChat.objects.filter(members=request.user,is_private=True)
  privateChats = []
  for chat in allPrivateChats:
    other_user = chat.members.exclude(id=request.user.id).first()
    other_user_avatar = Profile.objects.filter(user=other_user).first().avatar
    privateChats.append({
      'other_user':other_user.username,
      'other_user_avatar':other_user_avatar,
      'group_name':chat.group_name
    })
  
  # allPublicGroups = GroupChat.objects.filter(is_private=False)
  allPublicGroups = request.user.chat_groups.all()
  
  print("Groups",allPublicGroups)
  
  other_user = None
  if groupChat.is_private:
    if request.user not in groupChat.members.all():
      raise Http404
    for member in groupChat.members.all():
      if member != request.user:
        other_user = member
        print(other_user)
        break;
  
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
    
  context = {'avatar':avatar,
              'chats':chats,
              'form':form,
              'user': request.user,
              'other_user':other_user,
              'group_name':group_name,
              'private_chats':privateChats, 
              }

      
  return render(request, 'rtchat/index.html', context)


@login_required
def get_or_create_chatroom(request, username):
  if request.user.username == username:
      messages.error(request, 'User cannot create chatroom with themselves.')
      return redirect('index')

  other_user = User.objects.get(username=username)

  # Check if a private chatroom with both users already exists
  chatroom = GroupChat.objects.filter(
      is_private=True
  ).filter(members=request.user).filter(members=other_user).first()
  # If no chatroom exists, create a new one
  if not chatroom:
      chatroom = GroupChat.objects.create(is_private=True)
      chatroom.members.add(request.user, other_user)

  return redirect('chatroom', group_name=chatroom.group_name)

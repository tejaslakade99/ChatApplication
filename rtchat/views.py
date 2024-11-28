from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.db.models import OuterRef, Subquery, Max
from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request, group_name='Friends'):
  avatar = get_object_or_404(Profile, user__username=request.user.username)
  groupChat = get_object_or_404(GroupChat, group_name=group_name)
  if group_name != 'Friends' and request.user not in groupChat.members.all():
    return redirect('index')
  chats = GroupMessages.objects.filter(group=groupChat)
  form = ChatMessageCreateForm(request.POST)
  friendsGroup = GroupMessages.objects.filter(group__group_name = 'Friends').order_by('-created').first()
  allPrivateChats = GroupChat.objects.filter(members=request.user,is_private=True)
  
  last_private_message_subquery = GroupMessages.objects.filter(
    group=OuterRef('pk')
  ).order_by('-created').values('body', 'created')[:1]

# Annotate private chats with their last message
  allPrivateChats = allPrivateChats.annotate(
    last_message=Subquery(last_private_message_subquery.values('body')[:1]),
    time=Subquery(last_private_message_subquery.values('created')[:1])
  )
  
  allGroupChats = GroupChat.objects.filter(members=request.user,is_private=False).exclude(group_name='Friends')
  
      # Subquery to fetch the last message for each group
  last_message_subquery = GroupMessages.objects.filter(
      group=OuterRef('pk')
  ).order_by('-created').values('body','created')[:1]

  # Annotate groups with their last message
  allGroupChats = allGroupChats.annotate(
    last_message=Subquery(last_message_subquery.values('body')[:1]),
    time=Subquery(last_message_subquery.values('created')[:1])
)
  
  privateChats = []
  for chat in allPrivateChats:
    other_user = chat.members.exclude(id=request.user.id).first()
    other_user_avatar = Profile.objects.filter(user=other_user).first().avatar
    privateChats.append({
      'other_user':other_user.username,
      'other_user_avatar':other_user_avatar,
      'group_name':chat.group_name,
      'time':chat.time,
      'last_message':chat.last_message
    })
  
  # allPublicGroups = GroupChat.objects.filter(is_private=False)
  allPublicGroups = request.user.chat_groups.all()
  
  other_user = None
  if groupChat.is_private:
    if request.user not in groupChat.members.all():
      raise Http404
    for member in groupChat.members.all():
      if member != request.user:
        other_user = member
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
              'group_chat':groupChat,
              'all_group_chats':allGroupChats,
              'friendsGroup':friendsGroup,
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

def create_group_chat(request, group_name):
  group = GroupChat.objects.create(group_chat_name=group_name)
  group.admin = request.user
  group.members.add(request.user)
  group.save()
  return redirect('chatroom', group_name=group.group_name)
  
@login_required
def add_in_group(request, groupname):
  user = get_object_or_404(User, username=request.POST.get('user'))
  group = get_object_or_404(GroupChat, group_name=groupname)
  
  if group and user:
    group.members.add(user)
    group.save()
    
  online_users = group.users_online.all()
  members = group.members.all()
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
  # return HttpResponse("<h1>Hello WOrld</h1>")
  return render(request, 'partials/online_users_p2.html',{'online_users':online_users_with_avatars})

@login_required
def remove_in_group(request, groupname):
  user = get_object_or_404(User, username=request.POST.get('user'))
  group = get_object_or_404(GroupChat, group_name=groupname)
  allUsers = User.objects.all()
  
  if group and user:
    group.members.remove(user)
    group.save()

  online_users = group.users_online.all()
  members = group.members.all()
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
  return render(request, 'partials/online_users_p2.html',{'online_users':online_users_with_avatars})
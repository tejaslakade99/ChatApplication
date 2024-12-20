
# This class handles the presence of users in a group chat.
class PresenceService:
  @staticmethod
  def add_user(groupchat, user):
    if user not in groupchat.users_online.all():
      groupchat.users_online.add(user)
      groupchat.save()
      print("\n\n",groupchat.users_online.all())
      
  @staticmethod
  def remove_user(groupchat, user):
    if user in groupchat.users_online.all():
      groupchat.users_online.remove(user)
      groupchat.save()
      print("\n\n",groupchat.users_online.all())
  
  # Update the real-time presence of users in the group chat
  @staticmethod
  def update_online_users(groupchat):
    from rtchat.models import User, Profile
    members = groupchat.members.all() or User.objects.all()
    online_users = groupchat.users_online.all()
    print(groupchat.group_name, " members:", members, " online_users:", online_users)
    data = []
    for user in members:
      profile = Profile.objects.get(user=user)
      data.append({
        'username': user.username,
        'avatar': profile.avatar,
        'status': 'online' if user in online_users else 'offline'
      })
        
    return data
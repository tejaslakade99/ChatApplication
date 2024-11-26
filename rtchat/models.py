from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class GroupChat(models.Model):
  group_name = models.CharField(max_length=128, unique=True)

  def __str__(self):
    return self.group_name


class GroupMessages(models.Model):
  group = models.ForeignKey(GroupChat, related_name='group_messages', on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  body = models.CharField(max_length=300)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.author.username}: {self.body}'
  
  class Meta:
    ordering = ['-created']
    
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  avatar = models.URLField(max_length=500, blank=True, null=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')
  
  def __str__(self):
    return f"{self.user.username}'s profile"

# Signal to create a profile automatically
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Connect the signal to the User model
post_save.connect(create_profile, sender=User)
from django.db import models
from django.contrib.auth.models import User

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
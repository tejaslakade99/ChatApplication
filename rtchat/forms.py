from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreateForm(ModelForm):
  class Meta:
    model = GroupMessages
    fields = ['body']
    widgets = {
      'body':forms.TextInput(attrs={'placeholder':'Write your message...', 'maxlength':'300','autofocus':True})
    }
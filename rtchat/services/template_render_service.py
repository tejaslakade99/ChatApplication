from django.template.loader import render_to_string

# This service is responsible for rendering templates with the context provided.
class TemplateRenderService:
  
  @staticmethod
  def render_chat_message(chat, user):
    return render_to_string('partials/chat_message_p.html', context={
      'chat': chat,
      'user': user,
    })
    
  @staticmethod
  def render_online_users(online_users):
    return render_to_string('partials/online_users_p.html', context={
      'online_users': online_users,
    })
  
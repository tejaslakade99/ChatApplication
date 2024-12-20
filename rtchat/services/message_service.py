from rtchat.models import GroupMessages

# This class handles the creation of messages in the group chat.
class MessageService:
  @staticmethod
  def create_message(body, author, group):
    """
    Create a new message in the group chat.
    """
    try:
      message = GroupMessages.objects.create(
        body=body,
        author=author,
        group=group
      )
      return message
    except Exception as e:
      print(f"Error creating message: {e}")
      return None
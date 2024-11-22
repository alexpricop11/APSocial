from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Max
from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer, CreateChatSerializer
from chat.models import ChatMessage
from users.models import Users


class ChatService:

    def __init__(self, request, user):
        self.request = request
        self.user = user

    def get_chat_room(self):
        chat_rooms = ChatRoom.objects.filter(users__in=[self.user]).annotate(
            last_message_date=Max('chatmessage__date')
        ).order_by('-last_message_date')
        if chat_rooms:
            serializer = ChatRoomSerializer(chat_rooms, many=True, context={'request': self.request})
            return serializer.data
        return []

    def delete_chat(self, chat_id):
        chat_room = ChatRoom.objects.get(users=self.user, id=chat_id)
        if chat_room:
            chat_room.delete()
            return 'The chat has been deleted'
        raise ValidationError("Chat not found")

    def get_chat_messages(self, chat_id):
        try:
            chat_room = ChatRoom.objects.filter(id=chat_id, users__in=[self.user]).distinct().first()
            chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('date')
            serializer = ChatMessageSerializer(chat_messages, many=True, context={'request': self.request})
            return serializer.data
        except ObjectDoesNotExist:
            return []

    def create_chat(self, other_user_id):
        try:
            other_user = Users.objects.get(id=other_user_id)
            existing_chat = ChatRoom.objects.filter(users__in=[self.user, other_user]).distinct()
            if existing_chat.exists():
                chat_room = existing_chat.first()
                return {"id": chat_room.id, "name": chat_room.name}

            chat_name = other_user.username
            data = {
                'users': [self.user.id, other_user.id],
                'name': chat_name
            }
            serializer = CreateChatSerializer(data=data)
            if serializer.is_valid():
                chat_room = serializer.save()
                return {"id": chat_room.id, "name": chat_room.name}
            return serializer.errors

        except Exception as ex:
            return ex

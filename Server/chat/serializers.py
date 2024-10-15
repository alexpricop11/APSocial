from .models import ChatRoom, ChatMessage, UserChatName

from rest_framework import serializers


class ChatRoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField('get_name')
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'users', 'name', 'last_message']

    @staticmethod
    def get_users(obj):
        return [user.username for user in obj.users.all()]

    @staticmethod
    def get_last_message(obj):
        last_message = ChatMessage.objects.filter(chat_room=obj).latest('date')
        return LastMessageSerializer(last_message).data.get('message')

    def get_name(self, chat: ChatRoom):
        user = self.context['request'].user
        try:
            user_chat_name = UserChatName.objects.get(users=user, chat_room=chat)
            return user_chat_name.custom_name if user_chat_name.custom_name else chat.name
        except UserChatName.DoesNotExist:
            return chat.name


class LastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['message']


class ChatMessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_room', 'sender', 'message', 'date', 'seen']

    def get_chat_room(self, obj):
        user = self.context['request'].user
        chat_room = obj.chat_room
        try:
            user_chat_name = UserChatName.objects.get(users=user, chat_room=chat_room)
            return user_chat_name.custom_name if user_chat_name.custom_name else chat_room.name
        except UserChatName.DoesNotExist:
            return chat_room.name

    @staticmethod
    def get_sender(obj: ChatMessage):
        return obj.sender.username


class EditChatNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatName
        fields = ['custom_name']

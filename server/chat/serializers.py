from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'users', 'name']

    @staticmethod
    def get_users(obj):
        return [user.username for user in obj.users.all()]

    def get_name(self, obj):
        current_user = self.context['request'].user
        name_chat = [user for user in obj.users.all() if user != current_user]
        if name_chat:
            return ", ".join([user.username for user in name_chat])
        else:
            return ""


class ChatMessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_room', 'sender', 'message', 'date', 'seen']

    @staticmethod
    def get_sender(obj: ChatMessage):
        return obj.sender.username

    def get_chat_room(self, obj):
        current_user = self.context['request'].user
        other_users = [user for user in obj.chat_room.users.all() if user != current_user]
        if other_users:
            return ", ".join([user.username for user in other_users])
        return ""


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['users', 'name', 'created']


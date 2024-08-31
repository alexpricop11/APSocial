from .models import ChatRoom, ChatMessage

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

    def get_name(self, obj):
        current_user = self.context['request'].user
        name_chat = [user for user in obj.users.all() if user != current_user]
        if name_chat:
            return ", ".join([user.username for user in name_chat])
        else:
            return ""


class LastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['message']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_room', 'sender', 'message', 'date', 'seen']
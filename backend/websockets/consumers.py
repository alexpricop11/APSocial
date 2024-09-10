import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from users.models.user_online import UserOnline
from users.models.users import Users
from chat.models import ChatRoom, ChatMessage


class UserOnlineConsumers(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        await self.accept()
        await sync_to_async(UserOnline.objects.update_or_create)(
            user_id=self.user_id, defaults={'is_online': True, 'last_online': timezone.now()}
        )

    async def disconnect(self, close_code):
        await sync_to_async(UserOnline.objects.filter(user_id=self.user_id).update)(
            is_online=False, last_online=timezone.now()
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        online = data.get('online')
        return online


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_id = None

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(self.room_group_name, self.room_id)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json['sender']
        room_id = text_data_json['room_id']
        user = await sync_to_async(Users.objects.get)(username=sender)
        chat_room = await sync_to_async(ChatRoom.objects.get)(id=room_id)
        chat_message = await sync_to_async(ChatMessage.objects.create)(
            chat_room=chat_room, sender=user, message=message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'date': chat_message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'room_id': room_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        date = event['date']
        room_id = event['room_id']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'date': date,
            'room_id': room_id
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

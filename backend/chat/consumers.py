import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from users.models import Users


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_id = None

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
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

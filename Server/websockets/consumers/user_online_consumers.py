import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from users.models.user_online import UserOnline


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

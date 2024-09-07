from channels.generic.websocket import AsyncWebsocketConsumer
from .models.user_online import UserOnline
from django.utils import timezone


class UserOnlineConsumers(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.set_online_status(True)
            await self.accept()

    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.set_online_status(False)

    async def set_online_status(self, is_online):
        try:
            online_status, created = UserOnline.objects.get_or_create(user=self.user)
            online_status.is_online = is_online
            if not is_online:
                online_status.last_online = timezone.now()
            online_status.save()
        except UserOnline.DoesNotExist:
            pass

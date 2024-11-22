import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from users.models import Users

from notification.services import NotificationService


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        user_param = self.scope['url_route']['kwargs']['user']

        if not user_param:
            await self.close(code=400)
            return
        try:
            self.user = await sync_to_async(Users.objects.get)(id=user_param)
        except ObjectDoesNotExist:
            await self.close(code=404)
            return

        self.group_name = f"notifications_{self.user.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        notifications = await sync_to_async(NotificationService.get_notification)(self.user)
        notifications_json = json.dumps(notifications, default=str)
        await self.send(text_data=notifications_json)

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'create_notification':
            notification_type = data['type']
            message = data['message']
            notification = await sync_to_async(NotificationService.create_notification)(self.user, notification_type,
                                                                                        message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_notification",
                    "notification": {
                        "id": str(notification.id),
                        "user": str(self.user.id),
                        "type": notification_type,
                        "message": message,
                        "is_read": notification.is_read,
                        "timestamp": str(notification.timestamp),
                    },
                }
            )

        elif data['action'] == 'mark_as_read':
            notification_id = data['id']
            await sync_to_async(NotificationService.mark_as_read)(notification_id)

    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(text_data=json.dumps(notification))

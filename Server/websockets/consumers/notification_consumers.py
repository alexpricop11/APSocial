import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from notification.services import NotificationService


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    import json

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        sanitized_username = str(self.user).replace(" ", "_")
        self.group_name = f"notifications_{sanitized_username}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Fetch notifications asynchronously and convert UUIDs to strings
        notifications = await sync_to_async(NotificationService.get_notification)(self.user)

        # Convert UUIDs to strings
        notifications_json = json.dumps(notifications, default=str)
        await self.send(text_data=notifications_json)

    async def disconnect(self, close_code):
        # Ensure the user is authenticated before discarding from the group
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if not self.user.is_authenticated:
            return  # Ignore any messages from unauthenticated users

        if data['action'] == 'create_notification':
            notification_type = data['type']
            message = data['message']
            notification = NotificationService.create_notification(self.user, notification_type, message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_notification",
                    "notification": {
                        "id": notification.id,
                        "user": self.user.id,
                        "type": notification_type,
                        "message": message,
                        "is_read": notification.is_read,
                        "timestamp": str(notification.timestamp),
                    },
                }
            )

        elif data['action'] == 'mark_as_read':
            notification_id = data['id']
            NotificationService.mark_as_read(notification_id)

    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(text_data=json.dumps(notification))

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'content': data['content'],
            'message': data['message']
        }))

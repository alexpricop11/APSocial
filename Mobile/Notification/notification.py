import asyncio
import json

import flet as ft
import requests
import websockets


class Notification(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.websocket = None
        self.notifications = []
        self.token = None

    def get_token(self):
        self.token = self.page.client_storage.get('token')
        if self.token:
            asyncio.run(self.connect_websocket())

    async def connect_websocket(self):
        try:
            ws_url = f"ws://127.0.0.1:8000/ws/notifications/"
            self.websocket = await websockets.connect(ws_url, extra_headers={"Authorization": f"Bearer {self.token}"})
            await self.listen_notifications()

        except Exception as e:
            print(f"Connection error: {e}")

    async def listen_notifications(self):
        async for message in self.websocket:
            data = json.loads(message)
            if isinstance(data, list):
                self.notifications = [
                    self.create_notification_item(notif) for notif in data
                ]
            else:
                self.notifications.insert(0, self.create_notification_item(data))

            self.update_ui()

    @staticmethod
    def create_notification_item(notif):
        return ft.Column(
            [
                ft.Text(f"{notif['type']}: {notif['message']}", weight=ft.FontWeight.BOLD, size=16, no_wrap=False),
                ft.Text(f"{notif['timestamp']}", italic=True, size=12),
            ]
        )

    def update_ui(self):
        self.page.update()

    def build(self):
        self.get_token()
        return ft.SafeArea(ft.Column(self.notifications))

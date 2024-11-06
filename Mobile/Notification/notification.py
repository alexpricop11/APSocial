import json
import flet as ft
import websockets
import asyncio
import threading


class Notification(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.websocket = None
        self.token = None
        self.notification_container = ft.Column()

    def get_token_user_id(self):
        self.token = self.page.client_storage.get('token')
        self.user_id = self.page.client_storage.get('user_id')
        if self.token and self.user_id:
            threading.Thread(target=self.run_websocket_connection).start()

    def run_websocket_connection(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_websocket())
        loop.run_forever()

    async def connect_websocket(self):
        try:
            ws_url = f"ws://127.0.0.1:8000/ws/notifications/{self.user_id}/"
            headers = {"Authorization": f"Bearer {self.token}"}
            self.websocket = await websockets.connect(ws_url, extra_headers=headers)
            await self.listen_notifications()
        except Exception as e:
            print(f"Connection error: {e}")

    async def listen_notifications(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                self.update_ui(data)
        except Exception as e:
            print(f"Error receiving notifications: {e}")

    @staticmethod
    def create_notification_item(notif):
        # Format each notification item
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"{notif['type']}: {notif['message']}", weight=ft.FontWeight.BOLD, size=16, no_wrap=False),
                    ft.Text(f"{notif['timestamp']}", italic=True, size=12),
                ]
            ),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY),
            margin=5
        )

    def update_ui(self, notifications):
        self.notification_container.controls.clear()
        for notif in notifications:
            self.notification_container.controls.append(self.create_notification_item(notif))
        self.notification_container.update()

    def build(self):
        self.get_token_user_id()
        return ft.SafeArea(self.notification_container)

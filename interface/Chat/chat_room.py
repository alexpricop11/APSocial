import asyncio
import json

import flet as ft
import websockets
from api.api_client import APIClient


class ChatRoom(ft.UserControl):
    def __init__(self, room_id, token):
        super().__init__()
        self.api = APIClient()
        self.room_id = room_id
        self.token = token
        self.socket = None
        self.messages = []
        self.chat_name = None

    async def connect(self):
        url = f"ws://127.0.0.1:8000/ws/chat/{self.room_id}/"
        try:
            async with websockets.connect(url, extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                self.socket = websocket
                await self.receive_messages()
        except Exception as ex:
            print(ex)

    async def get_chat_name(self):
        response = self.api.chat_message(self.token, self.room_id)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                chat = data[0]
            else:
                chat = {}
            self.chat_name = chat.get('name', 'Unknown')
        else:
            self.chat_name = 'Error fetching chat name'
        self.page.update()

    async def receive_messages(self):
        async for message in self.socket:
            data = json.loads(message)
            self.messages.append(data)
            self.page.update()

    async def send_message(self, message):
        if self.socket:
            await self.socket.send(json.dumps(message))

    async def disconnect(self):
        if self.socket:
            await self.socket.close()
            self.socket = None

    def handle_disconnect(self, e):
        asyncio.create_task(self.disconnect())

    async def init_chat(self):
        await self.get_chat_name()
        await self.connect()

    def build(self):
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK)
        info_chat = ft.IconButton(icon=ft.icons.INFO)
        chat_name = ft.Text(self.chat_name, size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, expand=True,
                            text_align=ft.TextAlign.CENTER)
        return ft.SafeArea(
            ft.Row([
                back_button,
                chat_name,
                info_chat
            ])
        )

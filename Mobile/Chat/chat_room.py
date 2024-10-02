import asyncio
import json
from datetime import datetime

import flet as ft
import websockets
from .api_chat import APIChat
from .info_menu import InfoMenu


class ChatRoom(ft.UserControl):
    def __init__(self, room_id: int, token: str):
        super().__init__()
        self.date = None
        self.message_input = None
        self.api = APIChat()
        self.room_id = room_id
        self.token = token
        self.socket = None
        self.messages = []
        self.chat_name = None
        self.sender = None

    async def connect(self):
        url = f"ws://127.0.0.1:8000/ws/chat/{self.room_id}/"
        try:
            async with websockets.connect(url, extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                self.socket = websocket
                await self.receive_messages()
        except Exception as ex:
            print(ex)

    def get_chat_message(self):
        try:
            response = self.api.chat_message(self.token, self.room_id)
            if response.status_code == 200:
                data = response.json()
                self.chat_name = data[0].get('custom_name') or data[0]['chat_room']
                self.sender = data[0].get('sender')
                self.messages = data[0].get('message')
                self.date = data[0].get('date')
                print(self.messages)
            else:
                print('Error fetching chat name')
                self.messages = []
        except Exception as e:
            print(f"An error occurred: {e}")
            self.messages = []

    async def receive_messages(self):
        async for message in self.socket:
            data = json.loads(message)
            self.messages.append(data)
            self.update()

    async def send_message(self, message_data):
        if self.socket:
            try:
                await self.socket.send(json.dumps(message_data))
            except Exception as e:
                print(f"Error sending message: {e}")

    async def disconnect(self):
        if self.socket:
            await self.socket.close()
            self.socket = None

    def handle_disconnect(self, e):
        asyncio.create_task(self.disconnect())

    def go_back(self, e):
        self.page.views.pop()
        self.page.update()

    def info_menu(self, e):
        self.page.views.append(InfoMenu(self.token, self.room_id, self.chat_name))
        self.page.update()

    def app_bar(self, back_button, info_chat):
        return ft.Row([
            back_button,
            ft.Text(self.chat_name, text_align=ft.TextAlign.CENTER, expand=True, size=24,
                    color=ft.colors.random_color()),
            info_chat
        ])

    def chat_message(self):
        return ft.Column(
            controls=[ft.Text(f'{msg}') for msg in self.messages],
            height=self.page.window.height - 70
        )

    def input_message(self):
        self.message_input = ft.TextField(
            hint_text="Scrie un mesaj...",
        )
        return ft.Row([
            self.message_input,
            ft.IconButton(icon=ft.icons.SEND, on_click=self.on_send_message)
        ])

    def on_send_message(self, e):
        message = self.message_input.value
        if message:
            message_data = {
                'chat_room': self.room_id,
                "sender": self.sender,
                "message": message,
                'date': datetime.now()
            }
            print(message_data)
            self.send_message(message_data)
            self.message_input.value = ""
            self.message_input.update()

    def build(self):
        self.get_chat_message()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        info_chat = ft.IconButton(icon=ft.icons.INFO, on_click=self.info_menu)

        return ft.SafeArea(ft.Column([
            self.app_bar(back_button, info_chat),
            self.chat_message(), self.input_message()
        ]))

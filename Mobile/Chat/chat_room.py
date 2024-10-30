import asyncio
import json
import uuid
from datetime import datetime
from typing import Optional

import flet as ft
import websockets
from .api_chat import APIChat
from .info_menu import InfoMenu


class ChatRoom(ft.UserControl):
    def __init__(
            self,
            room_id,
            token,
            other_username: Optional[str] = None,
            other_user_id: Optional[uuid.UUID] = None
    ):
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
        self.other_user_id = other_user_id
        self.other_username = other_username

    async def connect(self):
        url = f"ws://127.0.0.1:8000/ws/chat/{self.room_id}/"
        try:
            async with websockets.connect(url, extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                self.socket = websocket
                print("WebSocket connection established")
                await self.receive_messages()
        except Exception as ex:
            print(f"WebSocket connection error: {ex}")

    def get_my_user_id(self):
        if self.page:
            self.sender = self.page.client_storage.get('user_id')

    def get_chat_message(self):
        response = self.api.chat_message(self.token, self.room_id)
        if response.status_code == 200:
            data = response.json()
            print(data)
            self.chat_name = data[0].get('chat_room')
            self.sender = data[0].get('sender', self.sender)
            self.messages = [msg['message'] for msg in data]
        elif response.status_code == 404:
            self.chat_name = self.other_username
            self.messages = []

    async def receive_messages(self):
        async for message in self.socket:
            data = json.loads(message)
            self.messages.append(data)
            self.update()  # Asigură-te că UI-ul se actualizează

    async def send_message(self, message_data):
        if self.socket:
            try:
                await self.socket.send(json.dumps(message_data))
                print(f"Message sent: {message_data}")
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

    def app_bar(self):
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        info_chat = ft.IconButton(icon=ft.icons.INFO, on_click=self.info_menu)

        return ft.Row([
            back_button,
            ft.Text(self.chat_name, text_align=ft.TextAlign.CENTER, expand=True, size=18),
            info_chat
        ])

    def chat_message(self):
        return ft.Column(
            controls=[ft.Text(f'{msg}') for msg in self.messages],
            height=self.page.window.height - 70
        )

    def input_message(self):
        self.message_input = ft.TextField(hint_text="Scrie un mesaj...")
        return ft.Column(
            controls=[
                ft.Row([
                    self.message_input,
                    ft.IconButton(
                        icon=ft.icons.SEND,
                        on_click=self.on_send_message
                    )]),
            ]
        )

    def on_send_message(self, e):
        message = self.message_input.value
        if message:
            print(message)
            if self.room_id is None:
                data = {'user_id': self.other_user_id}
                create_chat_response = self.api.create_chat(self.token, data)
                if create_chat_response.status_code == 201:
                    chat_data = create_chat_response.json()
                    self.room_id = chat_data.get('id')
                    self.chat_name = self.other_username
                else:
                    print("Failed to create or retrieve chat room.")
                    return

            message_data = {
                'chat_room': self.room_id,
                "sender": self.sender,
                "message": message,
                'date': datetime.utcnow().isoformat(),
                'seen': False
            }
            print(message_data)

            # Utilizează asyncio.create_task pentru a trimite mesajul
            asyncio.create_task(self.send_message(message_data))
            self.message_input.value = ""
            self.message_input.update()

    def build(self):
        self.get_my_user_id()
        self.get_chat_message()
        return ft.SafeArea(ft.Column([
            self.app_bar(),
            self.chat_message(), self.input_message()
        ]))

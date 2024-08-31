import asyncio
import json

import flet as ft
import websockets
from api.api_client import APIClient


class Chats(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.api = APIClient()
        self.token = None
        self.chats = []

    def get_token(self):
        self.token = self.page.client_storage.get("token")
        if self.token:
            self.get_chats()
        else:
            self.page.go('/auth')

    def get_chats(self):
        if not self.token:
            return
        response = self.api.chat_room(self.token)
        if response.status_code == 200:
            self.chats = response.json()
            self.chat_list()
        else:
            self.page.go('/auth')

    def chat_list(self):
        chat_list = []
        for chat in self.chats:
            chat_list.append(
                ft.ListTile(
                    title=ft.Text(chat['name'], size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    subtitle=ft.Text(
                        chat.get('last_message', ''),
                        chat.get('date'),
                        size=14,
                        color=ft.colors.GREY_500
                    ),
                    on_click=self.create_on_chat_room_click(chat['id'])))
        return ft.ListView(controls=chat_list, padding=10)

    def create_on_chat_room_click(self, chat_id):
        async def on_chat_room_click(e):
            await self.enter_chat_room(chat_id)

        return on_chat_room_click

    async def enter_chat_room(self, chat_id):
        chat_room = next((chat for chat in self.chats if chat['id'] == chat_id), None)
        if chat_room:
            room_id = chat_room['id']
            chat_room_view = ChatRoom(room_id=room_id, token=self.token)
            self.page.controls.append(chat_room_view)
            self.page.update()
            await chat_room_view.connect()

    def build(self):
        self.get_token()
        app_bar = ft.Container(
            ft.Row(controls=[
                ft.Text("CHAT", expand=True, text_align=ft.TextAlign.CENTER, size=24, color=ft.colors.GREEN),
                ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.GREY_50)
            ]),
            padding=10, margin=-10, bgcolor=ft.colors.BLACK)
        chat_list = self.chat_list()
        return ft.SafeArea(ft.Column([app_bar, chat_list]))


class ChatRoom(ft.UserControl):
    def __init__(self, room_id, token):
        super().__init__()
        self.room_id = room_id
        self.token = token
        self.socket = None
        self.messages = []

    async def connect(self):
        url = f"ws://127.0.0.1:8000/ws/chat/{self.room_id}/"
        try:
            async with websockets.connect(url, extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                self.socket = websocket
                await self.receive_messages()
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

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

    def build(self):
        message_list = [ft.Text(msg['message']) for msg in self.messages]
        return ft.SafeArea(ft.Column(
            controls=[
                message_list,
                ft.IconButton(icon=ft.icons.LOGOUT, on_click=self.handle_disconnect, icon_color=ft.colors.RED)
            ]
        ))

    def handle_disconnect(self, e):
        asyncio.create_task(self.disconnect())

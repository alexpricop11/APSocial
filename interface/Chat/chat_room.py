import asyncio
import json
import flet as ft
import websockets
from api.api_chat import APIChat
from .info_menu import InfoMenu


class ChatRoom(ft.UserControl):
    def __init__(self, room_id: int, token: str):
        super().__init__()
        self.api = APIChat()
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

    def get_chat_message(self):
        response = self.api.chat_message(self.token, self.room_id)
        if response.status_code == 200:
            data = response.json()
            self.chat_name = data[0].get('custom_name') or data[0]['chat_room']
            self.messages = data
        else:
            print('Error fetching chat name')

    async def receive_messages(self):
        async for message in self.socket:
            data = json.loads(message)
            self.messages.append(data)
            self.update()

    async def send_message(self, message):
        if self.socket:
            await self.socket.send(json.dumps(message))

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

    def build(self):
        self.get_chat_message()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        info_chat = ft.IconButton(icon=ft.icons.INFO, on_click=self.info_menu)
        top_bar = ft.Row([
            back_button,
            ft.Text(self.chat_name, text_align=ft.TextAlign.CENTER, expand=True, size=24,
                    color=ft.colors.random_color()),
            info_chat
        ])
        messages = ft.ListView(
            controls=[ft.Text(f"{msg['message']}") for msg in self.messages],
            spacing=10,
            auto_scroll=True,
        )
        input_send_message = ft.Row([
            ft.TextField(
                hint_text="Scrie un mesaj...",
                expand=True,
                autofocus=True,
                shift_enter=True,
                min_lines=1,
                max_lines=5,
                filled=True
            ),
            ft.IconButton(icon=ft.icons.SEND, on_click=None)
        ])
        return ft.SafeArea(ft.Column([
            top_bar, messages, input_send_message
        ],
            alignment=ft.alignment.bottom_center,
            horizontal_alignment=ft.CrossAxisAlignment.END
        ))

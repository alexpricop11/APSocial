import asyncio
import json

import flet as ft
import websockets

from api.api_chat import APIChat


class ChatRoom(ft.UserControl):
    def __init__(self, room_id, token):
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

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def toggle_info(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Editare Nume Chat"),
            content=ft.TextField(label="Numele nou al chat-ului", value=self.chat_name),
            actions=[
                ft.TextButton("Salvează", on_click=self.on_save_name),
                ft.TextButton("Anulează", on_click=self.close_dialog())
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def on_save_name(self, e):
        new_name = self.page.dialog.controls.value
        asyncio.create_task(self.edit_chat_name(new_name))
        self.page.dialog.open = False
        self.page.update()

    async def edit_chat_name(self, new_name):
        response = await self.api.edit_chat_name(self.token, self.room_id, new_name)
        if response.status_code == 200:
            self.chat_name = new_name
            self.update()
        else:
            print('Eroare la actualizarea numelui chat-ului')

    def build(self):
        self.get_chat_message()
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        info_chat = ft.IconButton(icon=ft.icons.INFO, on_click=None)
        top_bar = ft.Row([
            back_button,
            ft.Text(self.chat_name, text_align=ft.TextAlign.CENTER, expand=True, size=24,
                    color=ft.colors.random_color()),
            info_chat
        ])

        messages = ft.Column(
            controls=[ft.Text(f"{msg['message']}") for msg in self.messages]
        )
        input_send_message = ft.Container(content=ft.Row([
            ft.TextField(label="Scrie un mesaj...", height=40, width=250, expand=True),
            ft.IconButton(icon=ft.icons.SEND, on_click=None)
        ]), alignment=ft.alignment.bottom_center)

        return ft.SafeArea(ft.Column([top_bar, messages, input_send_message]))

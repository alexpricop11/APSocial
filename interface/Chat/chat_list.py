import flet as ft
from Chat.chat_room import ChatRoom
from api.api_chat import APIChat


class ChatList(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.chat_list_view = None
        self.api = APIChat()
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
                    leading=ft.Icon(
                        ft.icons.PERSON,
                        size=38,
                        color=ft.colors.WHITE
                    ),
                    title=ft.Text(chat.get('name'), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    subtitle=ft.Text(
                        chat.get('last_message', ''),
                        size=14,
                        color=ft.colors.GREY_500
                    ),
                    on_long_press=lambda e, chat_id=chat['id']: self.show_menu(chat_id, chat.get('name')),
                    on_click=lambda e, chat_id=chat['id']: self.open_chat(chat_id)))
        self.chat_list_view = ft.ListView(controls=chat_list)
        return self.chat_list_view

    def open_chat(self, chat_id):
        chat_room = ChatRoom(chat_id, self.token)
        self.page.controls.clear()
        self.page.views.append(chat_room)
        self.page.update()

    def handle_click(self, e):
        self.page.dialog.open = False
        self.page.update()

    def show_menu(self, chat_id, chat_name):
        action_sheet = ft.CupertinoActionSheet(
            title=ft.Row([ft.Text("Opțiuni")], alignment=ft.MainAxisAlignment.CENTER),
            message=ft.Row([ft.Text(f"Opțiuni pentru chat: {chat_name}")], alignment=ft.MainAxisAlignment.CENTER),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("Cancel"),
                on_click=self.handle_click,
            ),
            actions=[
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Șterge"),
                    is_destructive_action=True,
                    on_click=lambda e: self.delete_chat(chat_id),
                ),
            ],
        )
        bottom_sheet = ft.CupertinoBottomSheet(content=action_sheet)
        self.page.dialog = bottom_sheet
        self.page.dialog.open = True
        self.page.update()

    def delete_chat(self, chat_id):
        response = self.api.delete_chat(self.token, chat_id)
        if response.status_code == 200:
            self.chats = [chat for chat in self.chats if chat['id'] != chat_id]
            self.chat_list_view.controls.clear()
            self.chat_list_view.controls.extend([
                ft.ListTile(
                    leading=ft.Icon(
                        ft.icons.PERSON,
                        size=38,
                        color=ft.colors.WHITE if False else ft.colors.GREEN
                    ),
                    title=ft.Text(chat.get('name'), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    subtitle=ft.Text(
                        chat.get('last_message', ''),
                        size=14,
                        color=ft.colors.GREY_500
                    ),
                    on_long_press=lambda e, chat_id=chat['id']: self.show_menu(chat_id, chat.get('name')),
                    on_click=None)
                for chat in self.chats
            ])
            self.page.snack_bar = ft.SnackBar(ft.Text('Chat-ul a fost șters'), bgcolor='green')
            self.page.snack_bar.open = True
            self.page.dialog.open = False
            self.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text('Eroare la ștergere'), bgcolor='red')
            self.page.snack_bar.open = True
            self.page.dialog.open = False
        self.page.update()

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

import flet as ft
from Chat.chat_room import ChatRoom
from .api_chat import APIChat


class ChatList(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.api = APIChat()
        self.token = None
        self.chats = None

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
        elif response.status_code == 404:
            self.chats = []
        else:
            pass

    def create_on_click_handler(self, chat_id):
        return lambda e: self.open_chat(chat_id)

    def create_on_long_press_handler(self, chat_id, chat_name):
        return lambda e: self.show_menu(chat_id, chat_name)

    def chat_list(self):
        chat_list = [
            ft.ListTile(
                leading=ft.Icon(ft.icons.PERSON, size=38, color=ft.colors.WHITE),
                title=ft.Text(chat.get('name'), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                subtitle=ft.Text(
                    chat.get('last_message', '')[:20] + '...' if chat.get('last_message') and len(
                        chat.get('last_message', '')) > 20 else chat.get(
                        'last_message', ''),
                    size=14,
                    color=ft.colors.GREY_500),
                on_long_press=self.create_on_long_press_handler(chat['id'], chat.get('name')),
                on_click=self.create_on_click_handler(chat['id'])) for chat in self.chats
        ]
        return ft.ListView(
            controls=chat_list,
            height=self.page.window.height - 70,
        )

    def delete_chat(self, chat_id):
        response = self.api.delete_chat(self.token, chat_id)
        if response.status_code == 200:
            self.get_chats()
            self.show_snackbar('Chat-ul a fost șters', 'green')
        else:
            self.show_snackbar('Eroare la ștergere', 'red')
        self.close_dialog()
        self.page.update()

    def open_chat(self, chat_id):
        chat_room = ChatRoom(chat_id, self.token)
        self.page.controls.clear()
        self.page.views.append(chat_room)
        self.page.update()

    def close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()

    def show_menu(self, chat_id, chat_name):
        action_sheet = ft.CupertinoActionSheet(
            title=ft.Row([ft.Text("Opțiuni")], alignment=ft.MainAxisAlignment.CENTER),
            message=ft.Row([ft.Text(f"Opțiuni pentru chat: {chat_name}")], alignment=ft.MainAxisAlignment.CENTER),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("Cancel"),
                on_click=self.close_dialog,
            ),
            actions=[
                ft.CupertinoActionSheetAction(
                    content=ft.Text("Șterge"),
                    is_destructive_action=True,
                    on_click=lambda _: self.show_delete_confirmation(chat_id, chat_name)
                ),
            ],
        )
        bottom_sheet = ft.CupertinoBottomSheet(content=action_sheet)
        self.page.dialog = bottom_sheet
        self.page.dialog.open = True
        self.page.update()

    def show_delete_confirmation(self, chat_id, chat_name):
        dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Confirmare Ștergere"),
            content=ft.Text(f"Sunteți sigur că doriți să ștergeți chatul cu {chat_name}?"),
            actions=[
                ft.CupertinoDialogAction(
                    text="Anulează",
                    on_click=self.close_dialog
                ),
                ft.CupertinoDialogAction(
                    text="Confirmă",
                    is_destructive_action=True,
                    on_click=lambda _: self.delete_chat(chat_id)
                ),
            ]
        )
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    def show_snackbar(self, message, bgcolor):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=bgcolor)
        self.page.snack_bar.open = True
        self.page.update()

    def build(self):
        self.get_token()
        app_bar = ft.Container(
            ft.Row(controls=[
                ft.Text("CHAT", expand=True, text_align=ft.TextAlign.CENTER, size=24, color=ft.colors.GREEN),
                ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.GREY_50)
            ]), padding=10, margin=-10, bgcolor=ft.colors.BLACK)
        return ft.SafeArea(ft.Column([app_bar, self.chat_list()]))

import jwt
from api.api_chat import APIChat
import flet as ft


class InfoMenu(ft.UserControl):
    def __init__(self, token, chat_id, name_chat):
        super().__init__()
        self.api = APIChat()
        self.user_id = self.decode_token(token)
        self.chat_id = chat_id
        self.token = token
        self.name_chat = name_chat
        self.profile = ft.TextButton(
            content=ft.Column([
                ft.Icon(ft.icons.PERSON),
                ft.Text("Profil", size=10)
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=None
        )
        self.edit_chat_name = ft.TextButton(
            content=ft.Column([
                ft.Icon(ft.icons.EDIT),
                ft.Text("Editează numele", size=10)
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=self.edit_chat_name
        )
        self.block_user = ft.TextButton(
            content=ft.Column([
                ft.Icon(ft.icons.BLOCK, color='red'),
                ft.Text("Block", size=10)
            ], alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=self.block_user
        )

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            print('Token-ul a expirat')
        except jwt.InvalidTokenError:
            print('Token invalid')

    def edit_chat_name(self, e):
        new_name = ft.TextField(label="Editează numele", value=self.name_chat)

        def on_submit(e):
            data = {'custom_name': new_name.value}
            response = self.api.edit_chat_name(self.token, self.chat_id, data)
            if response.status_code == 200:
                self.name_chat = new_name.value
            else:
                self.show_snackbar('Eroare la editare numelui', 'red')
            self.close_dialog()

        content = ft.Column([
            new_name,
            ft.Row([
                ft.TextButton("Anulează", on_click=lambda _: self.close_dialog()),
                ft.TextButton("Confirmă", on_click=on_submit)
            ])
        ])
        self.show_dialog("Editează numele la chat", content)

    def block_user(self, e):
        data = {'user_id': self.user_id}
        response = self.api.block_user(self.token, data)
        if response == 200:
            self.show_snackbar('Utilizatorul a fost blocat', 'green')
            print(response.json())
        print(response.json())

    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def show_dialog(self, title, content):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Container(content, width=150, height=150))
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def go_back(self, e):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.update()

    def build(self):
        back = ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
        ])
        chat_name = ft.Text(f'Chat: {self.name_chat}', size=20, weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER)
        options = ft.Row([
            self.profile,
            self.edit_chat_name,
            self.block_user,
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.SafeArea(
            ft.Column(
                [
                    back,
                    ft.IconButton(ft.icons.PERSON, icon_size=50),
                    chat_name,
                    options
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

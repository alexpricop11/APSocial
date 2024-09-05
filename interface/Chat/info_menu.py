import flet as ft

from api.api_chat import APIChat


class InfoMenu(ft.UserControl):
    def __init__(self, token, chat_id, name_chat):
        super().__init__()
        self.api = APIChat()
        self.chat_id = chat_id
        self.token = token
        self.name_chat = name_chat
        self.edit_chat_name = ft.TextButton("Editează numele", icon=ft.icons.EDIT, on_click=self.edit_chat_name)
        self.block_user = ft.TextButton("Block", icon=ft.icons.BLOCK, icon_color='red')

    def edit_chat_name(self, e):
        new_name = ft.TextField(label="Editează numele", value=self.name_chat)

        def on_submit(e):
            data = {'custom_name': new_name.value}
            response = self.api.edit_chat_name(self.token, self.chat_id, data)
            if response.status_code == 200:
                self.name_chat = new_name.value
                print(response.json())
            else:
                print(f"Error: {response.json()}")
            self.close_dialog()

        content = ft.Column([
            new_name,
            ft.Row([
                ft.TextButton("Anulează", on_click=lambda _: self.close_dialog()),
                ft.TextButton("Confirmă", on_click=on_submit)
            ])
        ])
        self.show_dialog("Editează numele la chat", content)

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

        return ft.SafeArea(
            ft.Column(
                [
                    back,
                    chat_name,
                    self.edit_chat_name,
                    self.block_user,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

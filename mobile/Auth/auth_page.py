import flet as ft
from .register import Register
from .login import Login


class AuthPage(ft.View):
    def __init__(self):
        super().__init__()
        self.register = Register()
        self.login = Login()
        self.auth_button = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLACK,
            controls=[ft.Text('Înregistrare'), ft.Text('Login')],
            on_change=self.on_auth_button_change
        )
        self.content_container = ft.Container(content=self.register)

    def on_auth_button_change(self, e):
        if self.auth_button.selected_index == 0:
            self.content_container.content = self.register
        elif self.auth_button.selected_index == 1:
            self.content_container.content = self.login
        self.content_container.update()

    def build(self):
        welcome_text = ft.Text("Bun venit pe AP Social!", size=20, height=100, text_align=ft.TextAlign.CENTER)
        return ft.SafeArea(
            ft.Container(
                content=ft.Column([welcome_text, self.auth_button, self.content_container],
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10,
                alignment=ft.alignment.center,
            ),
        )

import flet as ft
from .api_auth import APIAuth


class Login(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.api = APIAuth()
        self.username = ft.TextField(label='Numele', width=200, on_change=self.validate)
        self.user_pass = ft.TextField(label='Parola', password=True, width=200, can_reveal_password=True,
                                      on_change=self.validate)
        self.login_button = ft.OutlinedButton(text='Login', width=200, on_click=self.login, disabled=True)

    def login(self, e):
        data = {
            'username': self.username.value.strip(),
            'password': self.user_pass.value.strip()
        }
        response = self.api.login(data)
        if response.status_code == 200:
            self.success_login(response)
        else:
            self.failed_login()

    def success_login(self, response):
        token = response.json().get("token")
        user_id = response.json().get("user_id")
        if self.page:
            self.page.client_storage.set("token", token)
            self.page.client_storage.set("user_id", user_id)
            self.page.go('/home')
        else:
            print("Page is not available.")

    def failed_login(self):
        self.page.snack_bar = ft.SnackBar(ft.Text('Numele sau parola nu este corectă sau nu există'), bgcolor='red')
        self.page.snack_bar.open = True
        self.page.update()

    def reset_password(self, e):
        self.page.go('/reset-password')

    def validate(self, e):
        is_password_valid = len(self.user_pass.value) >= 6 if self.user_pass.value else False
        self.login_button.disabled = not all([self.username.value, self.user_pass.value, is_password_valid])
        self.update()

    def build(self):
        reset_pass = ft.TextButton("Ai uitat parola?", on_click=self.reset_password)
        return ft.Column([self.username, self.user_pass, reset_pass, self.login_button],
                         alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

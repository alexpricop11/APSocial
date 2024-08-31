from api.api_client import APIClient
import flet as ft
import requests
import re


class Register(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.username = ft.TextField(label='Numele', width=200, on_change=self.validate)
        self.user_email = ft.TextField(label='Email', width=200, on_change=self.validate)
        self.phone_number = ft.TextField(label='Numărul de telefon', width=200, on_change=self.validate)
        self.birthday = ft.TextField(label='Data nașterii (Anul-Luna-Data)', width=200)
        self.user_pass = ft.TextField(label='Parola', password=True, width=200, can_reveal_password=True,
                                      on_change=self.validate)
        self.register_button = ft.OutlinedButton(text='Înregistrează-te', width=200, on_click=self.register,
                                                 disabled=True)
        self.api_client = APIClient()

    def register(self, e):
        data = {
            'username': self.username.value,
            'password': self.user_pass.value,
            'email': self.user_email.value,
            'phone_number': self.phone_number.value,
            'birthday': self.birthday.value
        }
        response = self.api_client.register(data)
        if response.status_code == 201:
            try:
                response_data = response.json()
                token = response_data.get("token")
                self.page.client_storage.set("token", token)
                self.page.go('/home')
            except requests.exceptions.JSONDecodeError:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f'Registration successful, but received invalid JSON response.'), bgcolor='yellow')
                self.page.snack_bar.open = True
                self.page.update()
        else:
            try:
                error_message = response.json()
            except requests.exceptions.JSONDecodeError:
                error_message = "Invalid response from server."
            self.page.snack_bar = ft.SnackBar(ft.Text(f'{error_message}'), bgcolor='red')
            self.page.snack_bar.open = True
            self.page.update()

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_number(number):
        pattern = r'^(\+\d{1,3}\s?)?\d{9,15}$'
        return re.match(pattern, number) is not None

    def validate(self, e):
        email_valid = self.is_valid_email(self.user_email.value) if self.user_email.value else True
        phone_valid = self.is_valid_number(self.phone_number.value) if self.phone_number.value else True
        password_valid = len(self.user_pass.value) >= 6 if self.user_pass.value else False
        self.register_button.disabled = not all(
            [self.username.value, self.user_pass.value, password_valid, email_valid, phone_valid, self.birthday])
        self.update()

    def build(self):
        return ft.Column(
            [self.username, self.user_pass, self.phone_number, self.user_email, self.birthday,
             self.register_button], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

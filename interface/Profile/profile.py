from api.api_client import APIClient
from datetime import datetime
import flet as ft
import requests


class UserProfile(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.token = None
        self.username = None
        self.my_followers = 0
        self.follow = 0
        self.birthday = None
        self.email = None
        self.phone_number = None

    def get_token(self):
        self.token = self.page.client_storage.get("token")
        if self.token:
            self.get_info_user()
        else:
            self.page.go('/auth')

    @staticmethod
    def format_date(date_str, from_format="%d/%m/%Y", to_format="%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, from_format).strftime(to_format)
        except ValueError:
            return date_str

    def get_info_user(self):
        response = self.api_client.get_user_profile(self.token)
        if response.status_code == 200:
            data = response.json()
            self.username = data.get('username')
            self.birthday = self.format_date(data.get('birthday')) if data.get('birthday') else ''
            self.email = data.get('email')
            self.my_followers = data.get('my_followers', 0)
            self.follow = data.get('follow', 0)
        else:
            self.show_snackbar(response.json().get('error'), 'red')

    def edit_profile(self, e):
        username_field = ft.TextField(label="Numele", value=self.username)
        email_field = ft.TextField(label="Email-ul", value=self.email)
        birthday_field = ft.TextField(label='Data nașterii (Anul-Luna-Data)', value=self.birthday)

        def on_submit(e):
            data = {
                'username': username_field.value,
                'email': email_field.value,
                'birthday': self.format_date(birthday_field.value)
            }
            self.update_user_profile(data)

        self.show_dialog('Editează profil-ul', ft.Column([
            username_field, email_field, birthday_field,
            ft.Row([
                ft.TextButton("Anulează", on_click=self.close_dialog),
                ft.TextButton("Confirmă", on_click=on_submit)
            ]),
            ft.Column()
        ]))

    def update_user_profile(self, data):
        try:
            response = self.api_client.edit_user_profile(self.token, data=data)
            response.raise_for_status()
            response_data = response.json()
            new_token = response_data.get('token')
            if new_token:
                self.page.client_storage.set("token", new_token)
                self.token = new_token
            self.show_snackbar('Profilul a fost actualizat', 'green')
            self.close_dialog()
            self.get_info_user()
            self.page.update()
        except requests.exceptions.RequestException as e:
            self.show_snackbar(f'Error: {e}', 'red')

    def change_password(self, e):
        current_password_field = ft.TextField(label='Parola actuală', password=True, can_reveal_password=True)
        new_password_field = ft.TextField(label='Parola nouă', password=True, can_reveal_password=True)

        def on_submit(e):
            current_password = current_password_field.value
            new_password = new_password_field.value
            self.update_password(current_password, new_password)

        self.show_dialog('Schimbă parola', ft.Column([
            current_password_field, new_password_field,
            ft.Row([
                ft.TextButton("Anulează", on_click=self.close_dialog),
                ft.TextButton("Confirmă", on_click=on_submit)
            ]),
            ft.Column()
        ]))

    def update_password(self, current_password, new_password):
        if len(new_password) < 6:
            self.show_snackbar('Parola trebuie să fie de cel puțin 6 caractere', 'red')
            return
        if new_password == current_password:
            self.show_snackbar('Noua parolă nu poate fi aceeași cu parola actuală', 'red')
            return

        data = {'password': current_password, 'new_password': new_password}
        response = self.api_client.change_password(self.token, data=data)
        if response.status_code == 200:
            self.show_snackbar("Parola a fost schimbată", 'green')
        else:
            self.show_error(response)

    def change_theme(self, e):
        new_theme = 'light' if self.page.theme_mode == 'dark' else 'dark'
        self.page.theme_mode = new_theme
        self.page.client_storage.set("theme_mode", new_theme)
        self.page.update()

    def logout(self, e):
        self.page.client_storage.remove("token")
        self.page.go('/auth')

    def close_dialog(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def show_dialog(self, title, content):
        self.page.dialog = ft.AlertDialog(title=ft.Text(title), content=content)
        self.page.dialog.open = True
        self.page.update()

    def show_error(self, response):
        try:
            error_texts = [ft.Text(f"{k}: {v}") for k, v in response.json().items()]
        except requests.exceptions.JSONDecodeError:
            error_texts = [ft.Text(response.json().get('error'))]
        self.page.dialog.controls.extend(error_texts)
        self.page.update()

    def show_user_info(self):
        profile = ft.Text(f'{self.username}', size=24, weight=ft.FontWeight.BOLD, expand=True)
        follow_text = ft.Text(f"Te urmărește:\n {self.my_followers}", size=16, color=ft.colors.GREY)
        followed_by_text = ft.Text(f"Urmărești:\n {self.follow}", size=16, color=ft.colors.GREY)
        popup_menu_button = self.create_popup_menu()
        button = ft.Row([profile, popup_menu_button], alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        user_info = ft.Row([follow_text, followed_by_text], alignment=ft.MainAxisAlignment.START, spacing=20)
        elements = [button, user_info]
        if self.birthday:
            user_birthday = ft.Text(f'Data de naștere: \n{self.birthday}', size=16)
            elements.append(user_birthday)
        return ft.Column(elements, alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    def create_popup_menu(self):
        return ft.PopupMenuButton(
            icon=ft.icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(text="Editează profil-ul", icon=ft.icons.DRAW, on_click=self.edit_profile),
                ft.PopupMenuItem(text="Schimbă parola", icon=ft.icons.PASSWORD, on_click=self.change_password),
                ft.PopupMenuItem(text="Schimbă tema", icon=ft.icons.BRIGHTNESS_6, on_click=self.change_theme),
                ft.PopupMenuItem(text="Ieșire", icon=ft.icons.LOGOUT, on_click=self.logout)
            ]
        )

    def build(self):
        self.get_token()
        profile = ft.Container(content=ft.Column(controls=[
            self.show_user_info()
        ]))
        return profile

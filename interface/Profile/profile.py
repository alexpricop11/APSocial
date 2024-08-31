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
            self.birthday = self.format_date(data.get('birthday'))
            self.email = data.get('email')
            self.my_followers = data.get('my_followers')
            self.follow = data.get('follow')
        else:
            self.show_snackbar(ft.Text(response.json().get('error')), 'red')

    def edit_profile(self, e):
        username_field = ft.TextField(label="Numele", value=self.username)
        email_field = ft.TextField(label="Email-ul", value=self.email)
        birthday_field = ft.TextField(label='Data nașterii (Anul-Luna-Data)', value=self.birthday)
        result = ft.Column()

        def on_submit(e):
            data = {
                'username': username_field.value,
                'email': email_field.value,
                'birthday': self.format_date(birthday_field.value)
            }
            response = self.api_client.edit_user_profile(self.token, data=data)
            if response.status_code == 200:
                response_data = response.json()
                new_token = response_data.get('token')
                if new_token:
                    self.page.client_storage.set("token", new_token)
                    self.token = new_token
                self.show_snackbar('Profilul a fost actualizat', 'green')
                self.get_info_user()
                self.close_dialog()
                self.update()
            else:
                result.controls.append(ft.Text(response.json().get('error')))
            self.page.update()
        content = ft.Column([username_field, email_field, birthday_field,
                             ft.Row([
                                 ft.TextButton("Anulează", on_click=lambda _: self.close_dialog()),
                                 ft.TextButton("Confirmă", on_click=on_submit)
                             ]),
                             result
                             ])
        self.show_dialog('Editează profil-ul', content=content)

    def change_password(self, e):
        current_password_field = ft.TextField(label='Parola actuală', password=True, can_reveal_password=True)
        new_password_field = ft.TextField(label='Parola nouă', password=True, can_reveal_password=True)
        result = ft.Column()

        def on_submit(e):
            current_password = current_password_field.value
            new_password = new_password_field.value
            if len(new_password) < 6:
                result.controls.append(ft.Text('Parola trebuie să fie de cel puțin 6 caractere'))
                self.page.update()
                return
            if new_password == current_password:
                result.controls.append(ft.Text('Noua parolă nu poate fi aceeași cu parola actuală'))
                self.page.update()
                return
            data = {
                'password': current_password,
                'new_password': new_password
            }
            response = self.api_client.change_password(self.token, data=data)
            if response.status_code == 200:
                self.show_snackbar("Parola a fost schimbată", 'green')
                self.close_dialog()
            elif response.status_code == 400:
                try:
                    errors = response.json()
                    error_texts = [ft.Text(f"{k}: {v}") for k, v in errors.items()]
                    result.controls.extend(error_texts)
                except requests.exceptions.JSONDecodeError:
                    result.controls.append(ft.Text(response.json().get('error')))
            elif response.status_code == 500:
                result.controls.append(ft.Text(response.json().get('error')))
            else:
                result.controls.append(ft.Text(response.json().get('error')))
            self.page.update()

        content = ft.Column([
            current_password_field,
            new_password_field,
            ft.Row([
                ft.TextButton("Anulează", on_click=lambda _: self.close_dialog()),
                ft.TextButton("Confirmă", on_click=on_submit)
            ]),
            result
        ])
        self.show_dialog('Schimbă parola', content=content)

    def change_theme(self, e):
        new_theme = 'light' if self.page.theme_mode == 'dark' else 'dark'
        self.page.theme_mode = new_theme
        self.page.client_storage.set("theme_mode", new_theme)
        self.page.update()

    def logout(self, e):
        self.page.client_storage.remove("token")
        self.page.go('/auth')

    def close_dialog(self):
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

    def show_user_info(self):
        profile = ft.Text(f'{self.username}', size=24, weight=ft.FontWeight.BOLD, expand=True)
        follow_text = ft.Text(f"Te urmărește:\n {self.my_followers}", size=16, color=ft.colors.GREY)
        followed_by_text = ft.Text(f"Urmărești:\n {self.follow}", size=16, color=ft.colors.GREY)
        user_birthday = ft.Text(f'Data de naștere: \n{self.birthday}', size=16)
        popup_menu_button = ft.PopupMenuButton(
            icon=ft.icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(text="Editează profil-ul", icon=ft.icons.DRAW, on_click=self.edit_profile),
                ft.PopupMenuItem(text="Schimbă parola", icon=ft.icons.PASSWORD, on_click=self.change_password),
                ft.PopupMenuItem(text="Schimbă tema", icon=ft.icons.BRIGHTNESS_6, on_click=self.change_theme),
                ft.PopupMenuItem(text="Ieșire", icon=ft.icons.LOGOUT, on_click=self.logout)])
        button = ft.Row(
            [profile, popup_menu_button],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20)
        user_info = ft.Row(
            [follow_text, followed_by_text],
            alignment=ft.MainAxisAlignment.START,
            spacing=20)
        user = ft.Column(
            [button, user_info, user_birthday],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15)
        return user

    def build(self):
        self.get_token()
        profile = ft.Container(content=ft.Column(controls=[
            self.show_user_info()
        ]))
        return profile

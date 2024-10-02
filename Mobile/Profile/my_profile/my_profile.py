from datetime import datetime
import flet as ft
import requests
from utils import show_dialog, show_snackbar
from .change_password import ChangePassword
from .edit_profile import EditProfile
from .my_profile_ui import UserProfileUI
from Profile.api_profile import APIProfile


class MyProfile(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.api_profile = APIProfile()
        self.token = None
        self.profile_photo = None
        self.username = None
        self.online = None
        self.my_followers = 0
        self.follow = 0
        self.birthday = None
        self.email = None
        self.phone_number = None
        self.ui = UserProfileUI(self)

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
        response = self.api_profile.get_user_profile(self.token)
        if response.status_code == 200:
            data = response.json()
            self.profile_photo = data.get('profile_image', None)
            self.username = data.get('username')
            self.online = data.get('online')
            self.birthday = self.format_date(data.get('birthday')) if data.get('birthday') else ''
            self.email = data.get('email')
            self.my_followers = data.get('my_followers', 0)
            self.follow = data.get('follow', 0)
        else:
            show_snackbar(self.page, response.json().get('error'), 'red')

    def edit_profile(self, e):
        EditProfile(self).edit_profile()

    def change_password(self, e):
        ChangePassword(self).change_password()

    def change_theme(self, e):
        new_theme = 'light' if self.page.theme_mode == 'dark' else 'dark'
        self.page.theme_mode = new_theme
        self.page.client_storage.set("theme_mode", new_theme)
        self.page.update()

    def logout(self, e):
        self.page.client_storage.remove("token")
        self.page.go('/auth')

    def show_error(self, response):
        error_texts = response.json().get('error')
        show_snackbar(self.page, error_texts, 'red')
        self.page.update()

    def close_dialog(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def build(self):
        self.get_token()
        return ft.Container(content=ft.Column(controls=[
            self.ui.show_user_info()
        ]))

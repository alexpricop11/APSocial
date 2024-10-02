import flet as ft
import requests
from utils import show_dialog, show_snackbar


class EditProfile:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def edit_profile(self):
        username_field = ft.TextField(label="Numele", value=self.user_profile.username)
        email_field = ft.TextField(label="Email-ul", value=self.user_profile.email)
        birthday_field = ft.TextField(label='Data nașterii (Anul-Luna-Data)', value=self.user_profile.birthday)

        def on_submit(e):
            data = {
                'username': username_field.value,
                'email': email_field.value,
                'birthday': self.user_profile.format_date(birthday_field.value)
            }
            self.update_user_profile(data)

        show_dialog(self.user_profile.page, 'Editează profil-ul', ft.Column([
            username_field, email_field, birthday_field,
            ft.Row([
                ft.TextButton("Anulează", on_click=self.user_profile.close_dialog),
                ft.TextButton("Confirmă", on_click=on_submit)
            ]),
            ft.Column()
        ]))

    def update_user_profile(self, data):
        try:
            response = self.user_profile.api_profile.edit_user_profile(self.user_profile.token, data=data)
            response.raise_for_status()
            response_data = response.json()
            new_token = response_data.get('token')
            if new_token:
                self.user_profile.page.client_storage.set("token", new_token)
                self.user_profile.token = new_token
            show_snackbar(self.user_profile.page, 'Profilul a fost actualizat', 'green')
            self.user_profile.close_dialog()
            self.user_profile.get_info_user()
            self.user_profile.page.update()
        except requests.exceptions.RequestException as e:
            show_snackbar(self.user_profile.page, f'Error: {e}', 'red')

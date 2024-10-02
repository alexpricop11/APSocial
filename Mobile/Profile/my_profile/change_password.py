import flet as ft
from utils import show_dialog, show_snackbar


class ChangePassword:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def change_password(self):
        current_password_field = ft.TextField(label='Parola actuală', password=True, can_reveal_password=True)
        new_password_field = ft.TextField(label='Parola nouă', password=True, can_reveal_password=True)

        def on_submit(e):
            current_password = current_password_field.value
            new_password = new_password_field.value
            self.update_password(current_password, new_password)

        show_dialog(self.user_profile.page, 'Schimbă parola', ft.Column([
            current_password_field, new_password_field,
            ft.Row([
                ft.TextButton("Anulează", on_click=self.user_profile.close_dialog),
                ft.TextButton("Confirmă", on_click=on_submit)
            ]),
            ft.Column()
        ]))

    def update_password(self, current_password, new_password):
        if len(new_password) < 6:
            show_snackbar(self.user_profile.page, 'Parola trebuie să fie de cel puțin 6 caractere', 'red')
            return
        if new_password == current_password:
            show_snackbar(self.user_profile.page, 'Noua parolă nu poate fi aceeași cu parola actuală', 'red')
            return

        data = {'password': current_password, 'new_password': new_password}
        response = self.user_profile.api_profile.change_password(self.user_profile.token, data=data)
        if response.status_code == 200:
            show_snackbar(self.user_profile.page, "Parola a fost schimbată", 'green')
            self.user_profile.close_dialog()
        else:
            self.user_profile.show_error(response)

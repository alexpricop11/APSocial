from .api_auth import APIAuth
import flet as ft


class ResetPassword(ft.View):
    def __init__(self):
        super().__init__()
        self.api = APIAuth()
        self.username = ft.TextField(label='Introduceți numele')
        self.request_button = ft.ElevatedButton("Trimite Codul", on_click=self.send_reset_code)
        self.back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)

    def send_reset_code(self, e):
        username = self.username.value.strip()
        if username:
            response = self.api.reset_password({'username': username})
            self.handle_response(response)
        else:
            self.show_snackbar('Introduceți un nume existent', 'red')

    def handle_response(self, response):
        if response.status_code == 200:
            self.page.client_storage.set('username', self.username.value)
            self.page.go('/verify-code')
            self.show_snackbar('Codul a fost trimis', 'green')
        else:
            self.show_snackbar('Eroare necunoscută', 'red')

    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def go_back(self, e):
        self.page.go('/auth')

    def build(self):
        selected_option = ft.Text("Scrie numele contului tău și vei primi un cod pe email pentru a reseta parola.", size=20,
                                  height=100, text_align=ft.TextAlign.CENTER)
        back_button = self.back_button
        text_back = ft.Column([back_button, selected_option])
        return ft.SafeArea(
            ft.Container(
                content=ft.Column([text_back, self.username, self.request_button],
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10,
                alignment=ft.alignment.center))


class VerifyCode(ft.View):
    def __init__(self):
        super().__init__()
        self.api = APIAuth()
        self.username = None
        self.back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_auth)
        self.reset_code = ft.TextField(label='Introduceți codul')
        self.new_password = ft.TextField(label='Introduceți parola nouă', password=True, can_reveal_password=True)
        self.reset_button = ft.ElevatedButton("Schimbă parola", on_click=self.reset_password)

    def reset_password(self, e):
        username = self.page.client_storage.get('username')
        code = self.reset_code.value
        new_password = self.new_password.value
        if username and code and new_password:
            response = self.api.verify_code({
                'username': username,
                'reset_code': code,
                'new_password': new_password
            })
            response_json = response.json()
            if response.status_code == 200:
                self.page.snack_bar = ft.SnackBar(ft.Text('Parola a fost actualizată'), bgcolor='green')
                self.page.overlay.append(self.page.snack_bar)
                self.page.snack_bar.open = True
                self.page.go('/auth')
                self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(response_json.get('error', 'Eroare la schimbarea parolei')),
                                                  bgcolor='red')
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text('Completează toate câmpurile.'), bgcolor='red')
            self.page.snack_bar.open = True
            self.page.update()


    def go_auth(self, e):
        self.page.go('/reset-password')

    def build(self):
        selected_option = ft.Text("Introduceți codul primit si parola nouă pentru a reseta parola.", size=20,
                                  height=100, text_align=ft.TextAlign.CENTER)
        back_button = self.back_button
        text_back = ft.Column([back_button, selected_option])
        return ft.SafeArea(ft.Column(
            controls=[text_back, self.reset_code, self.new_password, self.reset_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        ))

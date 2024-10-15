from Profile.api_profile import APIProfile
import flet as ft


class HisProfile(ft.UserControl):
    def __init__(self, token, user_id):
        super().__init__()
        self.followers_count = None
        self.following_count = None
        self.profile_image = None
        self.username = None
        self.token = token
        self.user_id = user_id
        self.api = APIProfile()

    def go_back(self, e):
        self.page.views.pop()
        self.page.update()

    def get_his_profile(self):
        response = self.api.his_profile(self.token, self.user_id)
        print(response)
        if response.status_code == 200:
            data = response.json()
            self.username = data.get('username')
            self.profile_image = data.get('profile_photo')
            self.followers_count = data.get('followers_count')
            self.following_count = data.get('following_count')
        else:
            self.username = 'Loading...'

    def build(self):
        self.get_his_profile()
        return ft.SafeArea(
            ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back), ft.Text(self.username, size=35),
                    ft.IconButton(icon=ft.icons.MORE_VERT, on_click=None)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Icon(ft.icons.PERSON, size=70),
                    ft.TextButton(f"Urmăritori:\n {self.followers_count}", style=ft.ButtonStyle(color='grey'), on_click=None),
                    ft.TextButton(f"Urmărește:\n {self.following_count}", style=ft.ButtonStyle(color='grey'), on_click=None)],
                    wrap=True),
                ft.Row([
                    ft.ElevatedButton(text='Urmărește', icon='add', width=150, on_click=None),
                    ft.ElevatedButton(text='Mesaj', icon="send", width=150, on_click=None),
                ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
            ]),
        )

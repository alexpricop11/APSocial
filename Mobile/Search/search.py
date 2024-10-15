import flet as ft

from .api_search import APISearchUser
from Profile.other_profile.other_profile import HisProfile


class Search(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.api = APISearchUser()
        self.token = None
        self.user_search = ft.SearchBar(
            bar_hint_text="Caută...",
            on_change=self.search
        )
        self.results_container = ft.Column()

    def search(self, e):
        self.token = self.page.client_storage.get("token")
        self.results_container.controls.clear()
        response = self.api.search_user(self.token, user=self.user_search.value)
        if response.status_code == 200:
            for user in response.json():
                user_id = user.get('id')
                username = user.get('username')
                self.results_container.controls.append(ft.ListTile(
                    title=ft.Text(f'{username}'),
                    on_click=lambda _, user_id=user_id: self.open_his_profile(user_id)
                ))
        elif response.status_code == 404:
            self.results_container.controls.append(ft.Text('', size=24))
        else:
            self.results_container.controls.append(ft.Text("Error: No response from server"))
        self.update()

    def open_his_profile(self, user_id):
        self.user_id = user_id
        his_profile = HisProfile(self.token, self.user_id)
        self.page.controls.clear()
        self.page.views.append(his_profile)
        self.page.update()

    def build(self):
        return ft.Column(
            controls=[
                self.user_search,
                self.results_container
            ]
        )

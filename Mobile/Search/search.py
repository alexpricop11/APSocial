import flet as ft
from Profile.other_profile.other_profile import HisProfile

from .api_search import APISearchUser


class Search(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.api = APISearchUser()
        self.token = None
        self.user_search = ft.SearchBar(
            bar_hint_text="Caută prieteni...",
            on_change=self.search
        )
        self.results_container = ft.Column()

    def get_token(self):
        self.token = self.page.client_storage.get("token")
        return self.token

    def search(self, e):
        self.results_container.controls.clear()

        if not self.user_search.value:
            self.get_history_search()
        else:
            response = self.api.search_user(self.token, user=self.user_search.value)
            if response.status_code == 200:
                users = response.json()
                self.success_search(users)
            elif response.status_code == 404:
                self.results_container.controls.append(ft.Text("No results found", size=24))
            else:
                self.results_container.controls.append(ft.Text(response.json()))

        self.update()

    def success_search(self, users):
        for user in users:
            user_id = user.get('id')
            username = user.get('username')
            self.results_container.controls.append(ft.ListTile(
                title=ft.Text(f'{username}'),
                on_click=lambda _, u_id=user_id: self.open_his_profile(u_id)
            ))

    def open_his_profile(self, user_id):
        self.save_history(user_id)
        self.user_id = user_id
        his_profile = HisProfile(self.token, self.user_id)
        self.page.controls.clear()
        self.page.views.append(his_profile)
        self.page.update()

    def get_history_search(self):
        response = self.api.get_history_search(self.token)
        self.results_container.controls.clear()
        if response.status_code == 200:
            history_data = response.json()
            self.success_get_history(history_data)
        elif response.status_code == 404:
            self.results_container.controls.append(ft.Text(""))
        else:
            self.results_container.controls.append(ft.Text(response.json()))

    def success_get_history(self, history_data):
        if history_data:
            self.results_container.controls.extend([
                ft.ListTile(
                    title=ft.Text(item['searched_user']),
                    trailing=ft.IconButton(
                        icon=ft.icons.CLOSE,
                        icon_size=30,
                        on_click=lambda _, user=item['searched_user']: self.remove_from_history(user)
                    ),
                    on_click=lambda _, user_id=item['id']: self.open_his_profile(self.user_id)
                ) for item in history_data
            ])
        else:
            self.results_container.controls.append(ft.Text("No search history available.", size=16))

    def remove_from_history(self, user):
        response = self.api.delete_user_from_history(self.token, user)
        if response.status_code == 200:
            self.get_history_search()
            self.update()
        else:
            print(response.json())

    def save_history(self, searched_user):
        response = self.api.save_user_history(self.token, searched_user)
        if response.status_code != 200:
            print(response.json())

    def build(self):
        self.get_token()
        self.get_history_search()
        return ft.Column(
            controls=[
                self.user_search,
                self.results_container
            ]
        )

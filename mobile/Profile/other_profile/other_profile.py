from Profile.api_profile import APIProfile
import flet as ft

from Chat.api_chat import APIChat

from Chat.chat_room import ChatRoom


class HisProfile(ft.UserControl):
    def __init__(self, token, user_id):
        super().__init__()
        self.is_follow = None
        self.followers_count = None
        self.following_count = None
        self.profile_image = None
        self.username = None
        self.token = token
        self.user_id = user_id
        self.api = APIProfile()
        self.api_chat = APIChat()
        self.follow_button_container = ft.Container()
        self.followers_text = ft.Text()

    def go_back(self, e):
        self.page.views.pop()
        self.page.update()

    def get_his_profile(self):
        response = self.api.his_profile(self.token, self.user_id)
        if response.status_code == 200:
            data = response.json()
            self.username = data.get('username')
            self.profile_image = data.get('profile_photo')
            self.followers_count = data.get('followers_count')
            self.following_count = data.get('following_count')
            self.is_follow = data.get('is_follow')
        else:
            self.username = 'Loading...'

    def follow(self, e):
        data = {'user_id': self.user_id}
        response = self.api.following_user(self.token, data)
        if response.status_code == 200:
            self.is_follow = not self.is_follow
            self.get_his_profile()
            self.update_ui()

    def follow_button(self):
        if self.is_follow:
            return ft.ElevatedButton(
                text='Urmărești',
                icon='person_remove',
                color='grey',
                width=150,
                on_click=self.follow
            )
        else:
            return ft.ElevatedButton(
                text='Urmărește',
                icon='person_add',
                width=150,
                on_click=self.follow
            )

    def open_chat(self, e):
        response = self.api_chat.chat_room(self.token)
        if response.status_code == 200:
            chat_rooms = response.json()
            for room in chat_rooms:
                if self.user_id in room['users']:
                    chat_id = room['id']
                    chat_room = ChatRoom(chat_id, self.token)
                    self.page.controls.clear()
                    self.page.views.append(chat_room)
                    self.page.update()

            chat_room = ChatRoom(None, self.token, self.username, self.user_id)
            self.page.controls.clear()
            self.page.views.append(chat_room)
            self.page.update()
        elif response.status_code == 404:
            chat_room = ChatRoom(None, self.token, self.username, self.user_id)
            self.page.controls.clear()
            self.page.views.append(chat_room)
            self.page.update()

    def open_chat_button(self):
        return ft.ElevatedButton(text='Mesaj', icon="send", width=150, on_click=self.open_chat)

    def update_ui(self):
        self.follow_button_container.content = self.follow_button()
        self.follow_button_container.update()

        self.followers_text.value = f"Urmăritori:\n {self.followers_count}"
        self.followers_text.update()

        self.update()

    def build(self):
        self.get_his_profile()
        return ft.SafeArea(
            ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back),
                    ft.Text(self.username, size=24),
                    ft.IconButton(icon=ft.icons.MORE_VERT, on_click=None)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Icon(ft.icons.PERSON, size=70),
                    self.followers_text,
                    ft.TextButton(f"Urmărește:\n {self.following_count}", style=ft.ButtonStyle(color='grey'),
                                  on_click=None)
                ], wrap=True),

                ft.Row([
                    self.follow_button_container,
                    self.open_chat_button(),
                ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
            ])
        )

    def did_mount(self):
        self.update_ui()

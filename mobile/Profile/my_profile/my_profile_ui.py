import flet as ft

from utils import show_dialog

from Profile.other_profile.other_profile import HisProfile


class UserProfileUI:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def show_user_info(self):
        user_status = self.user_status(self.user_name(), self.online_status())
        button = self.user_button(user_status)
        elements = [button, self.follow_buttons()]
        if self.user_profile.birthday:
            elements.append(self.user_birthday())

        return ft.Column(elements, alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    def user_name(self):
        return ft.Text(self.user_profile.username, size=24, weight=ft.FontWeight.BOLD)

    def online_status(self):
        return ft.CircleAvatar(bgcolor='green', radius=5) if self.user_profile.online else None

    def follow_buttons(self):
        profile_photo = ft.Image(src=self.user_profile.profile_photo, width=35, height=35)
        follow = ft.TextButton(f"Te urmărește:\n{self.user_profile.followers_count}",
                               on_click=self.list_followers,
                               style=ft.ButtonStyle(color='grey'))
        followed = ft.TextButton(f"Urmărești:\n{self.user_profile.following_count}",
                                 on_click=self.list_following,
                                 style=ft.ButtonStyle(color='grey'))
        return ft.Row([profile_photo, follow, followed], wrap=True)

    @staticmethod
    def user_status(name, online_status):
        user_status_elements = [name] + ([online_status] if online_status else [])
        return ft.Row(user_status_elements, expand=True)

    def user_button(self, user_status):
        return ft.Row(
            [user_status, self.create_popup_menu()],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def user_birthday(self):
        return ft.Text(f'Data de naștere: \n{self.user_profile.birthday}', size=16)

    def create_popup_menu(self):
        return ft.PopupMenuButton(
            icon=ft.icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(text="Editează profil-ul", icon=ft.icons.DRAW,
                                 on_click=self.user_profile.edit_profile),
                ft.PopupMenuItem(text="Schimbă parola", icon=ft.icons.PASSWORD,
                                 on_click=self.user_profile.change_password),
                ft.PopupMenuItem(text="Schimbă tema", icon=ft.icons.BRIGHTNESS_6,
                                 on_click=self.user_profile.change_theme),
                ft.PopupMenuItem(text="Ieșire", icon=ft.icons.LOGOUT, on_click=self.user_profile.logout)
            ]
        )

    def list_followers(self, e=None):
        followers_list = [
            ft.ListTile(
                title=ft.Text(follower['username']),
                on_click=lambda e, user_id=follower['user_id']: self.open_user_profile(user_id)
            )
            for follower in self.user_profile.followers
        ]
        show_dialog(
            self.user_profile.page,
            title=ft.Text("Lista de urmăritori"),
            content=ft.Column(followers_list)
        )

    def open_user_profile(self, user_id):
        profile_view = HisProfile(self.user_profile.token, user_id)
        self.user_profile.page.controls.clear()
        self.user_profile.page.views.append(profile_view)
        self.user_profile.page.update()

    def list_following(self, e=None):
        following_list = [
            ft.ListTile(
                title=ft.Text(following['username']),
                on_click=lambda e, user_id=following['user_id']: self.open_user_profile(user_id)
            )
            for following in self.user_profile.following]
        show_dialog(
            self.user_profile.page,
            title=ft.Text("Lista de urmăriri"),
            content=ft.Column(following_list))

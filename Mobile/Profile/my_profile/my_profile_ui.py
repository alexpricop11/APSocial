import flet as ft


class UserProfileUI:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def show_user_info(self):
        profile_image = ft.Icon(ft.icons.PERSON, size=30)
        name = ft.Text(f'{self.user_profile.username}', size=24, weight=ft.FontWeight.BOLD)
        online = ft.CircleAvatar(bgcolor='green', radius=5) if self.user_profile.online else None
        follow_text = ft.Text(f"Te urmărește:\n {self.user_profile.my_followers}", size=16, color=ft.colors.GREY)
        followed_by_text = ft.Text(f"Urmărești:\n {self.user_profile.follow}", size=16, color=ft.colors.GREY)
        user_status_elements = [profile_image, name]
        if online:
            user_status_elements.append(online)

        user_status = ft.Row(user_status_elements, expand=True)
        button = ft.Row([user_status, self.create_popup_menu()], alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        user_info = ft.Row([follow_text, followed_by_text], alignment=ft.MainAxisAlignment.START, spacing=20)
        elements = [button, user_info]
        if self.user_profile.birthday:
            user_birthday = ft.Text(f'Data de naștere: \n{self.user_profile.birthday}', size=16)
            elements.append(user_birthday)

        return ft.Column(elements, alignment=ft.MainAxisAlignment.CENTER, spacing=15)

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

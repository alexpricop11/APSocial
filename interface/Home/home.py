from Profile.profile import UserProfile
from Chat.chat import Chats
import flet as ft


class Home(ft.View):
    def __init__(self):
        super().__init__()
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label='Acasă'),
                ft.NavigationBarDestination(icon=ft.icons.CHAT_BUBBLE, label='Chat'),
                ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_CIRCLE, label='Profil')
            ], on_change=self.navigate, selected_index=0, height=65, width=100
        )
        self.content_container = ft.Container(HomePage())
        self.context = [self.content_container, self.navigation_bar]

    def navigate(self, e):
        index = e.control.selected_index
        content = None
        if index == 0:
            content = HomePage()
        elif index == 1:
            content = Chats()
        elif index == 2:
            content = UserProfile()
        self.show_content(content)

    def build(self):
        safe_area = ft.SafeArea(
            ft.Column([
                self.content_container
            ]),
        )
        return safe_area

    def show_content(self, content):
        self.content_container.content = content
        self.content_container.update()


class HomePage(ft.UserControl):
    def __init__(self):
        super().__init__()

    @staticmethod
    def app_bar():
        app_bar = ft.Container(
            ft.Row(controls=[
                ft.Text("AP Social", expand=True, text_align=ft.TextAlign.LEFT, size=20, color=ft.colors.GREEN),
                ft.IconButton(icon=ft.icons.CIRCLE_NOTIFICATIONS, icon_color=ft.colors.GREEN),
                ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.GREEN),
            ]
            ), padding=10, margin=-10
        )
        return app_bar

    def build(self):
        text = ft.Text('Acasă', size=25)
        appbar = ft.Container(ft.Column([
            self.app_bar(), text
        ]))
        return appbar

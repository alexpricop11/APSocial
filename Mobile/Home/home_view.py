from Chat.chat_list import ChatList
from .home_page import HomePage
import flet as ft
from Notification.notification import Notification

from Search.search import Search

from Profile.my_profile.my_profile import MyProfile


class HomeView(ft.View):
    def __init__(self):
        super().__init__()
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label='Acasă'),
                ft.NavigationBarDestination(icon=ft.icons.SEARCH, label='Caută'),
                ft.NavigationBarDestination(icon=ft.icons.CHAT_BUBBLE, label='Chat'),
                ft.NavigationBarDestination(icon=ft.icons.CIRCLE_NOTIFICATIONS, label='Notificări'),
                ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_CIRCLE, label='Profil'),
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
            content = Search()
        elif index == 2:
            content = ChatList()
        elif index == 3:
            content = Notification()
        elif index == 4:
            content = MyProfile()
        self.show_content(content)

    def show_content(self, content):
        self.content_container.content = content
        self.content_container.update()

    def build(self):
        safe_area = ft.SafeArea(
            ft.Column([
                self.content_container
            ]),
        )
        return safe_area

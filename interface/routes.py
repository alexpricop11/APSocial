from Auth.reset_password import ResetPassword, VerifyCode
from Auth.auth_page import AuthPage
from Home.home import Home
import flet as ft


def routes(page: ft.Page):
    def route_change(route):
        page.views.clear()
        if page.route == '/auth':
            page.views.append(AuthPage())
        elif page.route == '/reset-password':
            page.views.append(ResetPassword())
        elif page.route == '/verify-code':
            page.views.append(VerifyCode())
        elif page.route == '/home':
            page.views.append(Home())
        page.update()

    page.on_route_change = route_change

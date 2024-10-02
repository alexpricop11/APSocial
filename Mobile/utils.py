from Home.user_online import set_user_online
from Profile.api_profile import APIProfile
import asyncio
import flet as ft


def user_online(page):
    asyncio.run(set_user_online(page))


def get_theme_mode(page):
    saved_theme = page.client_storage.get("theme_mode")
    if saved_theme is None:
        saved_theme = "dark"
    page.theme_mode = saved_theme
    page.update()


def get_token(page):
    token = page.client_storage.get("token")
    if token:
        response = APIProfile().get_user_profile(token)
        if response.status_code == 200:
            page.go('/home')
        else:
            page.go('/auth')
    else:
        page.go('/auth')


def show_snackbar(page, message, color):
    page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
    page.snack_bar.open = True
    page.update()


def show_dialog(page, title, content):
    page.dialog = ft.AlertDialog(title=ft.Text(title), content=content)
    page.dialog.open = True
    page.update()

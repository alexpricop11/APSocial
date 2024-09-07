from api.api_client import APIClient
from routes import routes
import flet as ft


def main(page: ft.Page):
    saved_theme = page.client_storage.get("theme_mode")
    if saved_theme is None:
        saved_theme = "dark"
    page.theme_mode = saved_theme
    page.adaptive = True
    routes(page)
    token = page.client_storage.get("token")
    if token:
        response = APIClient().get_user_profile(token)
        if response.status_code == 200:
            page.go('/home')
        else:
            page.go('/auth')
    else:
        page.go('/auth')
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

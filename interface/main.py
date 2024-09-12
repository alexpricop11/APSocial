from utils import get_token, get_theme_mode, user_online
from routes import routes
import flet as ft


def main(page: ft.Page):
    page.title = 'APSocial'
    page.scroll = ft.ScrollMode.AUTO
    routes(page)
    get_token(page)
    user_online(page)
    get_theme_mode(page)
    page.adaptive = True
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

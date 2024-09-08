from interface.utils import get_token, get_theme_mode
from routes import routes
import flet as ft


def main(page: ft.Page):
    routes(page)
    get_token(page)
    get_theme_mode(page)
    page.adaptive = True
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

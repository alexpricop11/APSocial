import asyncio
from Home.user_online import set_user_online
from utils import get_token, get_theme_mode
from routes import routes
import flet as ft


def main(page: ft.Page):
    page.title = 'apsocial'
    page.icon = "assets/apsocial.png"
    page.scroll = ft.ScrollMode.AUTO
    page.window.height = 700
    page.window.width = 350
    permissions = ft.PermissionHandler()
    page.overlay.append(permissions)
    routes(page)
    get_theme_mode(page)
    get_token(page)
    asyncio.run(set_user_online(page))
    page.adaptive = True
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets", upload_dir="uploads")


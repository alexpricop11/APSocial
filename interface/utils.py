from Home.user_online import set_user_online
from api.api_client import APIClient
import asyncio


def user_online(page):
    asyncio.run(set_user_online(page))


def get_theme_mode(page):
    saved_theme = page.client_storage.get("theme_mode")
    if saved_theme is None:
        saved_theme = "dark"
    page.theme_mode = saved_theme


def get_token(page):
    token = page.client_storage.get("token")
    if token:
        response = APIClient().get_user_profile(token)
        if response.status_code == 200:
            page.go('/home')
        else:
            page.go('/auth')
    else:
        page.go('/auth')

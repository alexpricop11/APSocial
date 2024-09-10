from Home.user_online import UserOnline, handle_websocket
from api.api_client import APIClient


async def set_user_online(page):
    token = page.client_storage.get("token")
    if token:
        response = APIClient().get_user_profile(token)
        user_id = response.json().get("id")
        websocket_handler = UserOnline(token, user_id=user_id)
        await handle_websocket(websocket_handler)

        async def on_disconnect(e):
            await websocket_handler.close()

        page.on_close = on_disconnect


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

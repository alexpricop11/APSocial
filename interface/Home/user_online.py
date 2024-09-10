import json
import websockets

from api.api_client import APIClient


class UserOnline:
    def __init__(self, token, user_id):
        self.token = token
        self.websocket_url = f'ws://127.0.0.1:8000/ws/online_status/{user_id}/'
        self.websocket = None

    async def connect(self):
        try:
            async with websockets.connect(
                    self.websocket_url,
                    extra_headers={
                        "Authorization": f"Bearer {self.token}"}) as websocket:
                self.websocket = websocket
                await self.send_online_status(True)
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    return data
        except Exception as e:
            return e

    async def send_online_status(self, is_online):
        if self.websocket:
            data = json.dumps({'online': is_online})
            await self.websocket.send(data)

    async def close(self):
        if self.websocket:
            await self.send_online_status(False)
            await self.websocket.close()


async def handle_websocket(websocket_handler):
    await websocket_handler.connect()


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

import json
import websockets


class UserOnline:
    def __init__(self, token, user_id):
        self.token = token
        self.websocket_url = f'ws://127.0.0.1:8000/ws/online_status/{user_id}/'
        self.websocket = None

    async def connect(self):
        try:
            async with websockets.connect(self.websocket_url,
                                          extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                self.websocket = websocket
                print("Connected to WebSocket")
                await self.send_online_status(True)
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print(f"Received data: {data}")
                    except json.JSONDecodeError:
                        print("Failed to decode JSON message")
                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket connection closed")
                        break
        except Exception as e:
            print(f"WebSocket connection error: {e}")

    async def send_online_status(self, is_online):
        if self.websocket:
            data = json.dumps({'online': is_online})
            await self.websocket.send(data)
            print(f"Sent online status: {is_online}")

    async def close(self):
        if self.websocket:
            await self.send_online_status(False)
            await self.websocket.close()
            print("WebSocket connection closed")


async def handle_websocket(websocket_handler):
    await websocket_handler.connect()

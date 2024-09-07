from django.urls import re_path
from .consumers import UserOnlineConsumers

websocket_urlpatterns_online = [
    re_path(r'ws/online_status/$', UserOnlineConsumers.as_asgi()),
]

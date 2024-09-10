from django.urls import re_path
from .consumers import UserOnlineConsumers, ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/online_status/(?P<user_id>[0-9a-f-]+)/$', UserOnlineConsumers.as_asgi()),
    re_path(r'ws/chat/(?P<room_id>\d+)/$', ChatConsumer.as_asgi()),
]

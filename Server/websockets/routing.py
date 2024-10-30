from django.urls import re_path
from .consumers import chat_consumers, user_online_consumers, notification_consumers

websocket_urlpatterns = [
    re_path(r'ws/online_status/(?P<user_id>[0-9a-f-]+)/$', user_online_consumers.UserOnlineConsumers.as_asgi()),
    re_path(r'ws/chat/(?P<room_id>\d+)/$', chat_consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/', notification_consumers.NotificationConsumer)
]

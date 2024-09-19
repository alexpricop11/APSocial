from .views import chat_room, chat_message
from django.urls import path

urlpatterns = [
    path('chat-room', chat_room.ChatRoomView.as_view()),
    path('chat-message/<int:chat_id>/', chat_message.chat_message),
    path('delete-chat/<int:chat_id>/', chat_room.delete_chat),
    path('edit-chat-name/<int:chat_id>/', chat_room.edit_chat_name),
]

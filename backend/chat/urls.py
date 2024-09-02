from chat import views
from django.urls import path

urlpatterns = [
    path('chat-room', views.ChatRoomView.as_view()),
    path('chat-message/<int:chat_id>/', views.chat_message),
    path('delete-chat/<int:chat_id>/', views.delete_chat)
]

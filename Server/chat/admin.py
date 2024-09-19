from django.contrib import admin

from .models import ChatRoom, ChatMessage, UserChatName


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserChatName)
class UserChatNameAdmin(admin.ModelAdmin):
    pass

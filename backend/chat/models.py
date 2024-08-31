from users.models import Users
from django.db import models


class ChatRoom(models.Model):
    users = models.ManyToManyField(Users)
    name = models.CharField(max_length=35)
    created = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

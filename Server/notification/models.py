from django.db import models
from users.models import Users


class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.CharField(max_length=85)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.timestamp}: {self.message}'

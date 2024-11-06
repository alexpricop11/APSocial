from django.db import models
from users.models import Users


class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.timestamp}: {self.message}'

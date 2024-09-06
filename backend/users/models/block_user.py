from users.models.users import Users
from django.db import models


class BlockedUser(models.Model):
    blocker = models.ForeignKey(Users, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(Users, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocked} blocked {self.blocker}"

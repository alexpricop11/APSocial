from django.db import models

from .users import Users


class UserOnline(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='online_status')
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(null=True, blank=True)

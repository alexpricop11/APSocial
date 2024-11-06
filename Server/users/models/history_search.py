from django.db import models
from users.models import Users


class HistorySearch(models.Model):
    user = models.ForeignKey(Users, related_name='searches_made', on_delete=models.CASCADE)
    searched_user = models.ForeignKey(Users, related_name='searches_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.urls import path
from notification.views import get_notification

urlpatterns = [
    path('notification', get_notification)
]
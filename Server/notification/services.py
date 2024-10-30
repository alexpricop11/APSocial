from notification.models import Notification
from notification.serializers import NotificationSerializer


class NotificationService:
    @staticmethod
    def get_notification(user):
        notification = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notification, many=True)
        return serializer.data

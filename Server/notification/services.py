from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification
from .serializers import NotificationSerializer


class NotificationService:
    @staticmethod
    def get_notification(user):
        notifications = Notification.objects.filter(user=user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data

    @staticmethod
    def create_notification(user, notification_type, message):
        notification = Notification.objects.create(user=user, type=notification_type, message=message)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{user.id}",
            {
                "type": "send_notification",
                "notification": {
                    "id": notification.id,
                    "user": user.id,
                    "type": notification_type,
                    "message": message,
                    "is_read": notification.is_read,
                    "timestamp": str(notification.timestamp),
                },
            }
        )
        return notification

    @staticmethod
    def mark_as_read(notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

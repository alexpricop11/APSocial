from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.serializers.user_online import UserOnlineSerializer
from users.models.user_online import UserOnline
from users.models.users import Users


@api_view(['POST'])
def status_user(request):
    user_id = request.data.get('user_id')
    online = request.data.get('online')
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user_online, created = UserOnline.objects.get_or_create(user=user)
    user_online.is_online = online
    if not online:
        user_online.last_online = timezone.now()
    user_online.save()
    serializer = UserOnlineSerializer(user_online)
    return Response(serializer.data, status=status.HTTP_200_OK)

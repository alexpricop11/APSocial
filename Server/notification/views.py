from notification.services import NotificationService
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def get_notification(request):
    result = NotificationService.get_notification(request.user)
    if result:
        return Response(result, status=200)
    return Response([], status=404)

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.services.profile_service import ProfileService


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def blocked_users(request):
    user_id = request.data.get('user_id')
    service = ProfileService(request.user)
    result = service.block_user(user_id)
    if result:
        return Response(result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

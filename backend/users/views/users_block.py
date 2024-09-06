from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models.block_user import BlockedUser
from rest_framework.response import Response
from users.models.users import Users
from rest_framework import status


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def blocked_users(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user_to_block = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    blocked_user, created = BlockedUser.objects.get_or_create(blocker=request.user, blocked=user_to_block)
    if created:
        return Response({"detail": "User blocked successfully."}, status=status.HTTP_201_CREATED)
    return Response({"detail": "User already blocked."}, status=status.HTTP_200_OK)

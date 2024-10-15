from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models.users import Users


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def search_user(request, user):
    search = Users.objects.filter(username__icontains=user).exclude(username=request.user.username)
    if search.exists():
        users_data = [{"id": users.id, "username": users.username} for users in search]
        return Response(users_data, status=status.HTTP_200_OK)
    return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

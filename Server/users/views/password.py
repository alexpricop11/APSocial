from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models.users import Users

from users.services.user_service import UserService


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        UserService.change_password(
            user=request.user,
            password=request.data.get('password'),
            new_password=request.data.get('new_password')
        )
        return Response('Password changed successfully.', status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    try:
        result = UserService.reset_password(request.data.get('username'))
        return Response(result, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_code(request):
    try:
        result = UserService.verify_reset_code(
            username=request.data.get('username'),
            reset_code=request.data.get('reset_code'),
            new_password=request.data.get('new_password')
        )
        return Response(result, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models.users import Users
from users.services import get_user_email, password_reset


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    password = request.data.get('password')
    new_password = request.data.get('new_password')
    if not password or not new_password:
        return Response({'error': 'Both current and new passwords are required'}, status=400)
    if not user.check_password(password):
        return Response({'error': 'Current password is incorrect'}, status=400)
    if not new_password:
        return Response({'error': 'Empty new password'}, status=400)
    user.set_password(new_password)
    user.save()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    username = request.data.get('username')
    if not username:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return Response({'error': 'Username does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    get_user_email(user)
    return Response({'message': 'Reset code sent to email.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_code(request):
    username = request.data.get('username')
    reset_code = request.data.get('reset_code')
    new_password = request.data.get('new_password')
    if not username or not reset_code or not new_password:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Users.objects.get(username=username)
        password_reset(user, reset_code, new_password)
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
    except Users.DoesNotExist:
        return Response({'error': 'Username does not exist'}, status=status.HTTP_400_BAD_REQUEST)

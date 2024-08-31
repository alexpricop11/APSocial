from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from users.models import Users
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    EditUserProfileSerializer

from .services import get_user_email, password_reset

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class Register(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if Users.objects.filter(username=username).exists():
                return Response({'username': 'Username already exists'})
            user = serializer.save()
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            return Response({'token': token, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                if Users.objects.filter(username=username).exists():
                    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Username does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            login(request, user)
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            return Response({'token': token,
                             'username': user.username,
                             'message': 'User logged in successfully'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = EditUserProfileSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            return Response({'token': token, 'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
def change_password(request):
    user = request.user
    password = request.data.get('password')
    new_password = request.data.get('new_password')
    if not password or not new_password:
        return Response({'error', 'Both current and new passwords are required'})
    if not user.check_password(password):
        return Response({'error', 'Current password is incorrect'})
    if not new_password:
        return Response({'error', 'Empty new password'})
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

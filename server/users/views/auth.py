from django.contrib.auth import login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.auth import UserRegistrationSerializer, UserLoginSerializer

from users.services.user_service import UserService


class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token = UserService.generate_token(user)
            return Response({'token': token, 'user_id': user.id, 'message': 'User created successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = UserService.login_user(
                    username=request.data['username'],
                    password=request.data['password']
                )
                login(request, user)
            except Exception as ex:
                return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
            token = UserService.generate_token(user)
            return Response({'token': token, 'username': user.username, 'user_id': user.id,
                             'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

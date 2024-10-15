from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from users.serializers.profile import UserProfileSerializer, EditUserProfileSerializer, OtherProfileSerializer

from users.models.users import Users

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]
    serializer_class = EditUserProfileSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            return Response({'token': token, 'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OtherProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = OtherProfileSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(Users, id=user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

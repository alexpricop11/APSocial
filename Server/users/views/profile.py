from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.serializers.profile import UserProfileSerializer, EditUserProfileSerializer, OtherProfileSerializer
from users.models.users import Users

from users.services.profile_service import ProfileService


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]

    @staticmethod
    def get(request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            target_user = get_object_or_404(Users, id=user_id)
            profile_data = ProfileService.get_other_profile(request, target_user)
        else:
            profile_data = ProfileService.get_user_profile(request.user)
        return Response(profile_data, status=status.HTTP_200_OK)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]
    serializer_class = EditUserProfileSerializer

    @staticmethod
    def put(request):
        try:
            result = ProfileService(request.user, request.data)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

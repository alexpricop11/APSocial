from django.shortcuts import get_object_or_404
from users.models import Users
from users.models import UserOnline
from users.serializers.profile import UserProfileSerializer, OtherProfileSerializer, EditUserProfileSerializer
from users.services.user_service import UserService
from rest_framework.exceptions import ValidationError


class ProfileService:
    @staticmethod
    def get_user_profile(user):
        return UserProfileSerializer(user).data

    @staticmethod
    def update_user_profile(user, data):
        serializer = EditUserProfileSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            token = UserService.generate_token(user)
            return {
                'user_data': serializer.data,
                'token': token,
                'message': 'Profile updated successfully'
            }
        raise ValidationError(serializer.errors)

    @staticmethod
    def get_other_profile(request, target_user):
        serializer = OtherProfileSerializer(target_user, context={'request': request})
        return serializer.data

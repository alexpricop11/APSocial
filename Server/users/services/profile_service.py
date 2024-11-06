from rest_framework.exceptions import ValidationError
from users.serializers.profile import UserProfileSerializer, OtherProfileSerializer, EditUserProfileSerializer
from users.services.user_service import UserService
from users.models import Users
from notification.services import NotificationService
from users.models import BlockedUser


class ProfileService:
    def __init__(self, user):
        self.user = user
        self.notification = NotificationService

    def get_user_profile(self):
        return UserProfileSerializer(self.user).data

    def update_user_profile(self, data):
        serializer = EditUserProfileSerializer(self.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            token = UserService.generate_token(self.user)
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

    def follow_user(self, user_id):
        user_to_follow = Users.objects.get(id=user_id)
        if self.user.following.filter(id=user_to_follow.id).exists():
            self.user.following.remove(user_to_follow)
            return "User unfollowed successfully."
        else:
            self.user.following.add(user_to_follow)
            self.notification.create_notification(
                user_to_follow,
                'Urmărire',
                f'Utilizatorul {self.user} a inceput să vă urmărească')
            return "User followed successfully."

    def block_user(self, user_id):
        if not user_id:
            return 'User ID is required'
        try:
            user_to_block = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return "User doesn't exists"
        blocked_user, created = BlockedUser.objects.get_or_create(blocker=self.user, blocked=user_to_block)
        if created:
            return "User blocked"
        return 'User already blocked'


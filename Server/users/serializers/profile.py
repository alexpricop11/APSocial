from users.models.user_online import UserOnline
from rest_framework import serializers
from users.models.users import Users


class UserProfileSerializer(serializers.ModelSerializer):
    online = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'profile_image', 'username', 'my_followers', 'follow', 'birthday', 'email', 'online']

    @staticmethod
    def get_online(user):
        try:
            online_status = UserOnline.objects.get(user=user)
            return online_status.is_online
        except UserOnline.DoesNotExist:
            return False


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'birthday', 'profile_image']

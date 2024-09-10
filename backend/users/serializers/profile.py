from rest_framework import serializers
from users.models.users import Users

from users.models.user_online import UserOnline


class UserProfileSerializer(serializers.ModelSerializer):
    online = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'username', 'my_followers', 'follow', 'birthday', 'email', 'online']

    @staticmethod
    def get_online(user):
        online_status = UserOnline.objects.get(user=user)
        return online_status.is_online


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'birthday']

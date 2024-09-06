from rest_framework import serializers
from users.models.users import Users


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'my_followers', 'follow', 'birthday', 'email']


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'birthday']

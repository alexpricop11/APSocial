from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models.users import Users
from users.services.user_service import UserService


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    birthday = serializers.DateField(required=False, allow_null=True, format="%d-%m-%Y")

    class Meta:
        model = Users
        fields = ['username', 'password', 'email', 'phone_number', 'birthday']

    def create(self, validated_data):
        return UserService.register_user(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=6)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return user

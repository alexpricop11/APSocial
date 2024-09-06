from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models.users import Users


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'password', 'email', 'phone_number', 'birthday']

    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            birthday=validated_data['birthday'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=6)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        return user

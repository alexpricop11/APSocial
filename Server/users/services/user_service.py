from django.contrib.auth import authenticate
from django.db import transaction
from users.models import Users
from rest_framework_jwt.settings import api_settings
from django.core.exceptions import ValidationError
from users.logic import get_user_email, password_reset

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserService:

    @staticmethod
    @transaction.atomic
    def register_user(validated_data):
        username = validated_data['username']
        user = Users(
            username=username,
            email=validated_data.get('email', None),
            phone_number=validated_data.get('phone_number', None),
            birthday=validated_data.get('birthday', None)
        )
        if Users.objects.filter(username=username).exists():
            raise ValidationError('This user already exists')
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def login_user(username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            if Users.objects.filter(username=username).exists():
                raise ValidationError('Invalid password')
            else:
                raise ValidationError('Username does not exist')
        return user

    @staticmethod
    def generate_token(user):
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)
        return token

    @staticmethod
    def change_password(user, password, new_password):
        if not password or not new_password:
            raise ValidationError('Both current and new passwords are required')
        if not user.check_password(password):
            raise ValidationError('Current password is incorrect')
        if not new_password:
            raise ValidationError('Empty new password')
        if new_password == password:
            raise ValidationError("The new password cannot be the same as the new one")
        user.set_password(new_password)
        user.save()

    @staticmethod
    def reset_password(username):
        if not username:
            raise ValidationError('Username is required')
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise ValidationError('Username does not exist.')
        get_user_email(user)
        return 'Reset code sent to email.'

    @staticmethod
    def verify_reset_code(username, reset_code, new_password):
        if not username or not reset_code or not new_password:
            raise ValidationError('All fields are required')
        try:
            user = Users.objects.get(username=username)
            password_reset(user, reset_code, new_password)
            return 'Password reset successful'
        except Users.DoesNotExist:
            raise ValidationError('Username does not exist')

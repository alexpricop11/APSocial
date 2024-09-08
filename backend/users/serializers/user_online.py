from rest_framework import serializers

from users.models.user_online import UserOnline


class UserOnlineSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField()

    class Meta:
        model = UserOnline
        fields = ['user', 'is_online', 'last_online']

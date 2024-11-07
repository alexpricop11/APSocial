from rest_framework import serializers

from users.models import HistorySearch


class HistorySerializer(serializers.ModelSerializer):
    searched_user = serializers.SerializerMethodField()

    class Meta:
        model = HistorySearch
        fields = '__all__'

    @staticmethod
    def get_searched_user(obj):
        return {
            'user_id': obj.searched_user.id,
            'username': obj.searched_user.username
        }
from datetime import datetime
from django.shortcuts import get_object_or_404
from users.models import Users
from users.models import HistorySearch
from users.serializers.history_search import HistorySerializer


class SearchUserService:

    @staticmethod
    def search_user(user, username):
        search = Users.objects.filter(username__icontains=user).exclude(username=username)
        if search.exists():
            users_data = [{"id": users.id, "username": users.username} for users in search]
            return users_data
        return []

    @staticmethod
    def save_in_history(user, searched_username):
        try:
            searched_user = get_object_or_404(Users, id=searched_username)

            history = HistorySearch.objects.filter(user=user, searched_user=searched_user)
            if history.exists():
                history_instance = history.first()
                history_instance.timestamp = datetime.now()
                history_instance.save()
            else:
                history_instance = HistorySearch.objects.create(user=user, searched_user=searched_user)

            return HistorySerializer(history_instance).data
        except Users.DoesNotExist:
            return {"error": "Searched user not found"}

    @staticmethod
    def get_history(user):
        history = HistorySearch.objects.filter(user=user).order_by('-timestamp')
        serializer = HistorySerializer(history, many=True)
        return serializer.data

    @staticmethod
    def delete_history(searched_username):
        try:
            user_history = HistorySearch.objects.filter(searched_user__username=searched_username)
            if user_history.exists():
                user_history.delete()
                return {"message": "User history deleted successfully"}
            else:
                return {"error": "History not found"}
        except Exception as e:
            return {"error": str(e)}

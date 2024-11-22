from users.models.user_online import UserOnline
from rest_framework import serializers
from users.models.users import Users


class UserProfileSerializer(serializers.ModelSerializer):
    online = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = [
            'id', 'profile_image', 'username', 'birthday', 'email', 'online',
            'followers_count', 'following_count', 'followers', 'following'
        ]

    @staticmethod
    def get_online(user):
        try:
            online_status = UserOnline.objects.get(user=user)
            return online_status.is_online
        except UserOnline.DoesNotExist:
            return False

    @staticmethod
    def get_followers_count(user):
        return user.followers.count()

    @staticmethod
    def get_following_count(user):
        return user.following.count()

    @staticmethod
    def get_followers(user):
        return [follower.username for follower in user.followers.all()]

    @staticmethod
    def get_following(user):
        return [following_user.username for following_user in user.following.all()]


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'birthday', 'profile_image']


class OtherProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_follow = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'profile_image', 'username', 'followers_count', 'following_count', 'followers', 'following',
                  'is_follow']

    @staticmethod
    def get_followers_count(user):
        return user.followers.count()

    @staticmethod
    def get_following_count(user):
        return user.following.count()

    @staticmethod
    def get_followers(user):
        return [follower.username for follower in user.followers.all()]

    @staticmethod
    def get_following(user):
        return [following_user.username for following_user in user.following.all()]

    def get_is_follow(self, user):
        request = self.context.get('request')
        if request and request.user.following.filter(id=user.id).exists():
            return True
        return False

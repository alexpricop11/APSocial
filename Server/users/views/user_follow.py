from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.models import Users


class FollowingUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]

    def post(self, request):
        user_id = request.data.get('user_id')
        user_to_follow = Users.objects.get(id=user_id)
        if request.user.following.filter(id=user_to_follow.id).exists():
            request.user.following.remove(user_to_follow)
            return Response({"message": "User unfollowed successfully."}, status=status.HTTP_200_OK)
        else:
            request.user.following.add(user_to_follow)
            return Response({"message": "User followed successfully."}, status=status.HTTP_200_OK)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.services.profile_service import ProfileService


class FollowingUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_class = [JSONWebTokenAuthentication]

    @staticmethod
    def post(request):
        user_id = request.data.get('user_id')
        service = ProfileService(request.user)
        result = service.follow_user(user_id)
        return Response(result, status=200)

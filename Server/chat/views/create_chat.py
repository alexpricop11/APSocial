from chat.services import ChatService
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class CreateChat(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    @staticmethod
    def post(request):
        other_user_id = request.data.get('user_id')
        service = ChatService(request, request.user)
        result = service.create_chat(other_user_id)
        return Response(result, status=200)

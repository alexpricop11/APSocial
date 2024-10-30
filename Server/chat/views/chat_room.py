from chat.services import ChatService
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ChatList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    @staticmethod
    def get(request):
        service = ChatService(request, request.user)
        result = service.get_chat_room()
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def delete_chat(request, chat_id):
    service = ChatService(request, request.user)
    result = service.delete_chat(chat_id)
    if result:
        return Response(result, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def edit_chat_name(request, chat_id):
    ...

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from chat.services import ChatService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def chat_message(request, chat_id):
    service = ChatService(request, request.user)
    result = service.get_chat_messages(chat_id)
    if result:
        return Response(result, status=status.HTTP_200_OK)
    return Response([], status=status.HTTP_404_NOT_FOUND)

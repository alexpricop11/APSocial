from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from chat.models import ChatRoom, ChatMessage
from chat.serializers import ChatMessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def chat_message(request, chat_id):
    chat_room = ChatRoom.objects.get(users=request.user, id=chat_id)
    if chat_room is None:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
    chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('date')
    serializer = ChatMessageSerializer(chat_messages, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

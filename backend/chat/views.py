from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = ChatRoomSerializer

    def get(self, request):
        current_user = request.user
        chat_rooms = ChatRoom.objects.filter(users__in=[current_user]).annotate(
            last_message_date=Max('chatmessage__date')
        ).order_by('-last_message_date')
        serializer = self.serializer_class(chat_rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
async def chat_message(request, chat_id):
    user = request.user
    chat_room = ChatRoom.objects.filter(users=user, id=chat_id).first()
    if chat_room is None:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
    chat_messages = ChatMessage.objects.filter(chat_room=chat_room)
    serializer = ChatMessageSerializer(chat_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

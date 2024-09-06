from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ChatRoom, ChatMessage, UserChatName
from .serializers import ChatRoomSerializer, ChatMessageSerializer, EditChatNameSerializer


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
def chat_message(request, chat_id):
    chat_room = ChatRoom.objects.get(users=request.user, id=chat_id)
    if chat_room is None:
        return Response({'error': 'Chat room not found'}, status=status.HTTP_404_NOT_FOUND)
    chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('date')
    serializer = ChatMessageSerializer(chat_messages, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def delete_chat(request, chat_id):
    chat_room = ChatRoom.objects.get(users=request.user, id=chat_id)
    if chat_room:
        chat_room.delete()
        return Response({'message': 'The chat has been deleted'}, status=status.HTTP_200_OK)
    return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def edit_chat_name(request, chat_id):
    chat_room = ChatRoom.objects.get(id=chat_id)
    custom_name, created = UserChatName.objects.get_or_create(users=request.user, chat_room=chat_room)
    serializer = EditChatNameSerializer(custom_name, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

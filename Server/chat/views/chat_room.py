from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = ChatRoomSerializer

    def get(self, request):
        current_user = request.user
        chat_rooms = ChatRoom.objects.filter(users__in=[current_user]).annotate(
            last_message_date=Max('chatmessage__date')
        ).order_by('-last_message_date')
        if chat_rooms:
            serializer = self.serializer_class(chat_rooms, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status.HTTP_404_NOT_FOUND)


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
    ...

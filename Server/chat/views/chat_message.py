from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from chat.models import ChatRoom, ChatMessage
from chat.serializers import ChatMessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def chat_message(request, chat_id):
    try:
        chat_room = ChatRoom.objects.filter(id=chat_id, users__in=[request.user]).distinct().first()
        chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('date')
        serializer = ChatMessageSerializer(chat_messages, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_404_NOT_FOUND)

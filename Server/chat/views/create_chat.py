from chat.serializers import CreateChatSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from chat.models import ChatRoom
from users.models import Users


class CreateChat(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = CreateChatSerializer

    def post(self, request):
        try:
            user = request.user
            other_user_id = request.data.get('user_id')

            other_user = Users.objects.get(id=other_user_id)
            if other_user == user:
                return Response(
                    {"error": "You cannot create a chat with yourself."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificăm dacă există deja o cameră cu acești utilizatori
            existing_chat = ChatRoom.objects.filter(users__in=[user, other_user]).distinct()
            if existing_chat.exists():
                chat_room = existing_chat.first()
                return Response(
                    {"id": chat_room.id, "name": chat_room.name},
                    status=status.HTTP_200_OK
                )

            # Dacă nu există o cameră, o creăm
            chat_name = other_user.username
            data = {
                'users': [user.id, other_user.id],
                'name': chat_name
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                chat_room = serializer.save()
                return Response(
                    {"id": chat_room.id, "name": chat_room.name},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Users.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            print(ex)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

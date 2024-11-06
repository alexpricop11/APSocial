from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from users.services.search_service import SearchUserService


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def search_user(request, user):
    result = SearchUserService.search_user(user, request.user.username)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_history(request):
    try:
        result = SearchUserService.get_history(request.user)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def save_user_in_history(request):
    try:
        searched_username = request.data.get('searched_username')
        if not searched_username:
            return Response({"error": "No username provided"}, status=status.HTTP_400_BAD_REQUEST)
        result = SearchUserService.save_in_history(request.user, searched_username)
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_from_history(request):
    try:
        searched_username = request.data.get('searched_user')
        if not searched_username:
            return Response({"error": "No username provided"}, status=status.HTTP_400_BAD_REQUEST)
        result = SearchUserService.delete_history(searched_username)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .serializers import UserSerializer


@api_view(["GET"])
def user_info(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({})  # 未登入回傳空物件


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "Logged out successfully"})

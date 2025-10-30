# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .serializers import UserSerializer


@api_view(["GET"])
def user_info(request):
    if request.user.is_authenticated:
        user = User.objects.select_related("paddle_user").get(pk=request.user.pk)
        serializer = UserSerializer(user)
        print("Serialized user info: ", serializer.data)
        return Response(serializer.data)
    return Response({})  # 未登入回傳空物件


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "Logged out successfully"})

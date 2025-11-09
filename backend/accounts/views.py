# accounts/views.py
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(["GET"])
def user_info(request):
    if request.user.is_authenticated:
        user = User.objects.select_related("paddle_user").get(pk=request.user.pk)
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)
    return Response({})  # 未登入回傳空物件


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "Logged out successfully"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    profile = request.user.profile
    profile.avatar = request.data["avatar"]
    profile.save()
    return Response({"avatar_url": request.build_absolute_uri(profile.avatar.url)})

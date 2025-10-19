from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


def home(request):
    return render(request, "home.html")


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer

    def get_permissions(self):
        """
        列表公開，但 retrieve 文章內容需要登入
        """

        if self.action == "list":
            return [AllowAny()]
        else:  # retrieve, create, update, delete
            return [IsAuthenticated()]

from django.shortcuts import render, get_object_or_404
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


def home(request):
    return render(request, "home.html")


# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, "home.html", {"posts": posts})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, "post_detail.html", {"post": post})


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
